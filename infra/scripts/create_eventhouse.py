#!/usr/bin/env python3
"""
Create EventHouse and execute schema in Microsoft Fabric
Integrates with existing solution accelerator deployment automation
"""

import os
import sys
import json
import requests
import time
from typing import Optional, Dict, Any

class FabricEventHouseDeployer:
    def __init__(self, workspace_id: str, eventhouse_name: str = "fabrikam_eventhouse"):
        self.workspace_id = workspace_id
        self.eventhouse_name = eventhouse_name
        self.base_url = "https://api.fabric.microsoft.com/v1"
        self.access_token = None
        
    def get_access_token(self) -> str:
        """Get access token for Fabric API"""
        import subprocess
        try:
            result = subprocess.run([
                'az', 'account', 'get-access-token', 
                '--resource', 'https://analysis.windows.net/powerbi/api',
                '--query', 'accessToken', '-o', 'tsv'
            ], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to get access token: {e}")

    def create_eventhouse(self) -> Dict[str, Any]:
        """Create EventHouse in the workspace"""
        if not self.access_token:
            self.access_token = self.get_access_token()
            
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "displayName": self.eventhouse_name,
            "type": "EventHouse"  # Fabric item type for EventHouse
        }
        
        url = f"{self.base_url}/workspaces/{self.workspace_id}/items"
        
        print(f"🏛️ Creating EventHouse: {self.eventhouse_name}")
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            eventhouse_info = response.json()
            print(f"✅ EventHouse created successfully: {eventhouse_info.get('id')}")
            return eventhouse_info
            
        except requests.exceptions.RequestException as e:
            if response.status_code == 409:
                print(f"ℹ️  EventHouse {self.eventhouse_name} already exists")
                return self.get_existing_eventhouse()
            else:
                raise Exception(f"Failed to create EventHouse: {e}")

    def get_existing_eventhouse(self) -> Dict[str, Any]:
        """Get existing EventHouse info"""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        url = f"{self.base_url}/workspaces/{self.workspace_id}/items"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        items = response.json().get('value', [])
        for item in items:
            if item.get('displayName') == self.eventhouse_name and item.get('type') == 'EventHouse':
                return item
                
        raise Exception(f"EventHouse {self.eventhouse_name} not found")

    def execute_kql_file(self, kql_file_path: str) -> bool:
        """Execute KQL file to create schema"""
        if not os.path.exists(kql_file_path):
            raise FileNotFoundError(f"KQL file not found: {kql_file_path}")
            
        print(f"📋 Executing KQL schema from: {kql_file_path}")
        
        with open(kql_file_path, 'r', encoding='utf-8') as f:
            kql_content = f.read()
        
        # Parse KQL commands (simplified - split by control commands)
        import re
        commands = []
        
        # Split by lines starting with . (KQL control commands)
        lines = kql_content.split('\n')
        current_command = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            if line.startswith('.') and current_command:
                # Start of new command, save previous
                cmd = '\n'.join(current_command).strip()
                if cmd:
                    commands.append(cmd)
                current_command = [line]
            else:
                current_command.append(line)
        
        # Don't forget the last command
        if current_command:
            cmd = '\n'.join(current_command).strip()
            if cmd:
                commands.append(cmd)
        
        print(f"🔄 Parsed {len(commands)} KQL commands")
        
        # Execute commands
        success_count = 0
        for i, command in enumerate(commands, 1):
            if self.execute_kql_command(command):
                success_count += 1
            else:
                print(f"⚠️  Command {i} failed, continuing...")
        
        print(f"📊 Executed {success_count}/{len(commands)} commands successfully")
        return success_count == len(commands)

    def execute_kql_command(self, command: str) -> bool:
        """Execute single KQL command"""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "db": self.eventhouse_name,
            "csl": command
        }
        
        url = f"{self.base_url}/workspaces/{self.workspace_id}/kqldatabases/{self.eventhouse_name}/query"
        
        try:
            print(f"Executing: {command[:80]}...")
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            if result.get('error'):
                print(f"❌ KQL Error: {result['error']}")
                return False
            
            print("✅ Success")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return False

def main():
    """Main deployment function"""
    if len(sys.argv) < 2:
        print("Usage: python create_eventhouse.py <workspace_id> [eventhouse_name] [kql_file]")
        sys.exit(1)
    
    workspace_id = sys.argv[1]
    eventhouse_name = sys.argv[2] if len(sys.argv) > 2 else "fabrikam_eventhouse"
    kql_file = sys.argv[3] if len(sys.argv) > 3 else "./src/eventhouse/table_creation.kql"
    
    print(f"🚀 Starting EventHouse deployment")
    print(f"🏢 Workspace ID: {workspace_id}")
    print(f"🏛️ EventHouse: {eventhouse_name}")
    print(f"📄 KQL File: {kql_file}")
    
    try:
        deployer = FabricEventHouseDeployer(workspace_id, eventhouse_name)
        
        # Step 1: Create EventHouse
        eventhouse_info = deployer.create_eventhouse()
        
        # Step 2: Execute schema
        if deployer.execute_kql_file(kql_file):
            print("🎉 EventHouse deployment completed successfully!")
            return 0
        else:
            print("⚠️  Schema deployment completed with some errors")
            return 1
            
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())