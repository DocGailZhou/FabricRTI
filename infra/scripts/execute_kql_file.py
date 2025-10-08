# Execute KQL Files using Azure Data Explorer Client Libraries
# Production-ready script for azd template integration
# This approach uses the official Kusto client libraries

import os
import sys
import json
import time
import re
from datetime import datetime
from typing import List, Tuple, Optional

try:
    from azure.kusto.data import KustoClient, KustoConnectionStringBuilder, ClientRequestProperties
    from azure.kusto.data.exceptions import KustoServiceError
    from azure.identity import DefaultAzureCredential, ClientSecretCredential
except ImportError:
    print("❌ Missing required packages. Install with:")
    print("   pip install azure-kusto-data azure-identity")
    sys.exit(1)

class KqlFileExecutor:
    def __init__(self, workspace_id: str, eventhouse_name: str, tenant_id: Optional[str] = None, 
                 client_id: Optional[str] = None, client_secret: Optional[str] = None):
        self.workspace_id = workspace_id
        self.eventhouse_name = eventhouse_name
        
        print(f"🔧 Initializing KQL executor for EventHouse: {eventhouse_name}")
        
        # Build Kusto connection string for Fabric EventHouse
        # Updated format for Fabric: https://{workspace}.kusto.fabric.microsoft.com
        cluster_uri = f"https://{workspace_id}.kusto.fabric.microsoft.com"
        
        print(f"🔗 Connecting to: {cluster_uri}")
        
        try:
            if client_id and client_secret and tenant_id:
                print("🔐 Using Service Principal authentication")
                kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
                    cluster_uri, client_id, client_secret, tenant_id
                )
            else:
                print("🔐 Using Default Azure credential (Azure CLI/Managed Identity)")
                # For azd deployments, use Azure CLI authentication
                kcsb = KustoConnectionStringBuilder.with_aad_device_authentication(cluster_uri)
            
            self.kusto_client = KustoClient(kcsb)
            print("✅ Kusto client initialized successfully")
            
        except Exception as e:
            print(f"❌ Failed to initialize Kusto client: {e}")
            raise
        
    def read_kql_file(self, file_path: str) -> List[str]:
        """Read and parse KQL file into individual commands with enhanced parsing"""
        print(f"📋 Reading KQL file: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"KQL file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print(f"📄 File size: {len(content)} characters")
        
        # Enhanced KQL command parsing
        commands = []
        
        # Split by command patterns - more sophisticated parsing
        # Pattern 1: Commands starting with . (control commands)
        control_command_pattern = r'(?m)^(\.(?:create|alter|drop|show|set).*?)(?=\n\.|\n\n|$)'
        
        # Pattern 2: Multi-line table creation commands
        table_create_pattern = r'(?s)(\.create table.*?\))\s*(?=\n\.|\n\n|$)'
        
        # Pattern 3: JSON mapping commands
        mapping_pattern = r'(?s)(\.create table.*?ingestion.*?mapping.*?\'\]\')\s*(?=\n\.|\n\n|$)'
        
        # Pattern 4: Policy commands
        policy_pattern = r'(?m)(\.alter table.*?policy.*?)(?=\n\.|\n\n|$)'
        
        # Pattern 5: Print and let statements
        query_pattern = r'(?m)^((?:print|let).*?)(?=\n\.|\n\n|$)'
        
        # Extract commands using patterns
        all_patterns = [
            mapping_pattern,    # JSON mappings first (they're complex)
            table_create_pattern,  # Table creation
            policy_pattern,     # Policy commands
            control_command_pattern,  # Other control commands
            query_pattern       # Query statements
        ]
        
        used_positions = set()
        
        for pattern in all_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                start, end = match.span()
                if not any(pos in range(start, end) for pos in used_positions):
                    command = match.group(1).strip()
                    if command and not command.startswith('//'):
                        commands.append(command)
                        used_positions.update(range(start, end))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_commands = []
        for cmd in commands:
            cmd_normalized = re.sub(r'\s+', ' ', cmd.strip())
            if cmd_normalized not in seen and len(cmd_normalized) > 5:  # Filter out very short commands
                seen.add(cmd_normalized)
                unique_commands.append(cmd)
        
        print(f"🔄 Parsed {len(unique_commands)} unique KQL commands")
        
        # Log command types for debugging
        command_types = {}
        for cmd in unique_commands:
            cmd_type = cmd.split()[0] if cmd.split() else 'unknown'
            command_types[cmd_type] = command_types.get(cmd_type, 0) + 1
        
        print(f"� Command breakdown: {command_types}")
        
        return unique_commands
    
    def execute_kql_command(self, command: str, retry_count: int = 3) -> Tuple[bool, str]:
        """Execute a single KQL command with retry logic"""
        command_preview = command.replace('\n', ' ')[:100] + ('...' if len(command) > 100 else '')
        
        for attempt in range(retry_count):
            try:
                if attempt > 0:
                    print(f"🔄 Retry attempt {attempt + 1}/{retry_count}")
                    time.sleep(2 ** attempt)  # Exponential backoff
                
                print(f"Executing: {command_preview}")
                
                # Set client request properties with appropriate timeouts
                client_request_properties = ClientRequestProperties()
                client_request_properties.set_option("servertimeout", "00:10:00")  # 10 minutes
                client_request_properties.set_option("request_timeout", "00:15:00")  # 15 minutes total
                
                # Execute command
                response = self.kusto_client.execute(
                    self.eventhouse_name, 
                    command, 
                    client_request_properties
                )
                
                print("✅ Success")
                return True, "Success"
                
            except KustoServiceError as e:
                error_msg = str(e)
                print(f"❌ Kusto Service Error: {error_msg}")
                
                # Check if it's a retryable error
                if "timeout" in error_msg.lower() or "throttle" in error_msg.lower():
                    if attempt < retry_count - 1:
                        print(f"⏳ Retryable error, will retry...")
                        continue
                
                return False, f"Kusto Error: {error_msg}"
                
            except Exception as e:
                error_msg = str(e)
                print(f"❌ General Error: {error_msg}")
                
                # Check if it's a connectivity issue
                if "connection" in error_msg.lower() or "network" in error_msg.lower():
                    if attempt < retry_count - 1:
                        print(f"🌐 Network error, will retry...")
                        continue
                
                return False, f"General Error: {error_msg}"
        
        return False, f"Failed after {retry_count} attempts"
    
    def execute_kql_file(self, file_path):
        """Execute entire KQL file"""
        print(f"🚀 Starting KQL file execution")
        print(f"📄 File: {file_path}")
        print(f"🏛️ EventHouse: {self.eventhouse_name}")
        print(f"⏰ Started: {datetime.now()}")
        
        try:
            commands = self.read_kql_file(file_path)
            
            success_count = 0
            error_count = 0
            errors = []
            
            for i, command in enumerate(commands, 1):
                print(f"\n📋 Command {i}/{len(commands)}:")
                success, result = self.execute_kql_command(command)
                
                if success:
                    success_count += 1
                else:
                    error_count += 1
                    errors.append(f"Command {i}: {result}")
            
            # Summary
            print(f"\n📊 EXECUTION SUMMARY:")
            print(f"✅ Successful commands: {success_count}")
            print(f"❌ Failed commands: {error_count}")
            print(f"📄 Total commands: {len(commands)}")
            
            if error_count > 0:
                print(f"\n❌ ERRORS:")
                for error in errors:
                    print(f"  - {error}")
            
            return error_count == 0
            
        except Exception as e:
            print(f"❌ Script execution failed: {e}")
            return False

# Usage example
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python execute_kql_file.py <workspace_id> <eventhouse_name> <kql_file_path>")
        sys.exit(1)
    
    workspace_id = sys.argv[1]
    eventhouse_name = sys.argv[2]
    kql_file_path = sys.argv[3]
    
    # Optional: Service Principal credentials from environment variables
    tenant_id = os.environ.get('AZURE_TENANT_ID')
    client_id = os.environ.get('AZURE_CLIENT_ID')
    client_secret = os.environ.get('AZURE_CLIENT_SECRET')
    
    executor = KqlFileExecutor(
        workspace_id=workspace_id,
        eventhouse_name=eventhouse_name,
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )
    
    success = executor.execute_kql_file(kql_file_path)
    sys.exit(0 if success else 1)