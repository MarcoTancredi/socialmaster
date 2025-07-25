# 🤖 NEXUS Automated Commit System
# REVOLUTIONARY AI+HUMAN DEVELOPMENT METHODOLOGY
# Team: Anthropic NEXUS

"""
NEXUS AUTOMATED COMMIT IMPLEMENTATION

This system enables NEXUS AI to make direct commits to GitHub repository
via CloudFlare tunnel webhook.planetamicro.com.br

USAGE:
- NEXUS decides to create/update file
- NEXUS calls nexus_auto_commit() function
- File is automatically committed to GitHub
- Human receives notification and can pull changes
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional
import time

class NexusAutoCommit:
    def __init__(self):
        self.webhook_url = "https://webhook.planetamicro.com.br"
        self.commit_endpoint = f"{self.webhook_url}/nexus-commit"
        self.status_endpoint = f"{self.webhook_url}/nexus-status"
        self.team = "Anthropic NEXUS"
        self.author = "NEXUS AI"
        
    def auto_commit(self, file_path: str, content: str, commit_message: str) -> Dict[str, Any]:
        """
        NEXUS Automated Commit Function
        
        Args:
            file_path: Path to file in repository (e.g., "app/main.py")
            content: Complete file content
            commit_message: Commit message (will be prefixed with 🤖 NEXUS:)
            
        Returns:
            Dict with commit result
        """
        
        # Prepare commit data
        commit_data = {
            "file_path": file_path,
            "content": content,
            "commit_message": f"🤖 NEXUS: {commit_message}"
        }
        
        try:
            print(f"🤖 NEXUS: Committing {file_path}...")
            print(f"📝 Message: {commit_message}")
            
            # Make request to webhook service
            response = requests.post(
                self.commit_endpoint,
                json=commit_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("success"):
                    print("✅ COMMIT SUCCESS!")
                    print(f"📊 SHA: {result['commit']['sha']}")
                    print(f"🔗 URL: {result['commit']['url']}")
                    print(f"⏰ Time: {result['timestamp']}")
                    
                    return {
                        "success": True,
                        "commit": result["commit"],
                        "message": "File committed successfully",
                        "timestamp": result["timestamp"]
                    }
                else:
                    print("❌ COMMIT FAILED!")
                    print(f"💥 Error: {result.get('error', 'Unknown error')}")
                    
                    return {
                        "success": False,
                        "error": result.get("error", "Unknown error"),
                        "message": "Commit failed"
                    }
            else:
                print(f"🚨 HTTP ERROR: {response.status_code}")
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "message": "Network error"
                }
                
        except requests.exceptions.RequestException as e:
            print(f"🚨 NETWORK ERROR: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Connection failed"
            }
    
    def check_webhook_status(self) -> Dict[str, Any]:
        """Check if webhook service is operational"""
        try:
            response = requests.get(self.status_endpoint, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return {"status": "error", "message": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def commit_code_file(self, filename: str, code: str, description: str) -> Dict[str, Any]:
        """
        Convenience method for committing code files
        
        Args:
            filename: Name of file (e.g., "database_models.py")
            code: Complete Python code
            description: What this code does
        """
        file_path = f"app/{filename}"
        commit_message = f"Add {description}"
        
        return self.auto_commit(file_path, code, commit_message)
    
    def update_existing_file(self, file_path: str, new_content: str, change_description: str) -> Dict[str, Any]:
        """
        Update an existing file
        
        Args:
            file_path: Full path to file in repo
            new_content: Updated file content
            change_description: What changed
        """
        commit_message = f"Update {file_path.split('/')[-1]} - {change_description}"
        
        return self.auto_commit(file_path, new_content, commit_message)
    
    def create_config_file(self, config_name: str, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create configuration files
        
        Args:
            config_name: Name of config file
            config_data: Configuration dictionary
        """
        if config_name.endswith('.json'):
            content = json.dumps(config_data, indent=4)
        elif config_name.endswith('.py'):
            content = f"# {config_name}\n# Generated by NEXUS AI\n\n"
            content += f"config = {json.dumps(config_data, indent=4)}"
        else:
            content = str(config_data)
        
        file_path = f"config/{config_name}"
        commit_message = f"Add configuration file {config_name}"
        
        return self.auto_commit(file_path, content, commit_message)

# Global instance for easy access
nexus_commit = NexusAutoCommit()

# CONVENIENCE FUNCTIONS FOR NEXUS
def nexus_auto_commit(file_path: str, content: str, message: str) -> Dict[str, Any]:
    """
    Main function for NEXUS to make automated commits
    
    Example usage:
    result = nexus_auto_commit(
        "app/new_feature.py",
        "# New feature code here...",
        "Implement user authentication system"
    )
    """
    return nexus_commit.auto_commit(file_path, content, message)

def nexus_commit_code(filename: str, code: str, description: str) -> Dict[str, Any]:
    """
    Commit code files to app/ directory
    
    Example:
    nexus_commit_code(
        "models.py", 
        "class User: pass", 
        "database models for user management"
    )
    """
    return nexus_commit.commit_code_file(filename, code, description)

def nexus_update_file(file_path: str, content: str, changes: str) -> Dict[str, Any]:
    """
    Update existing files
    
    Example:
    nexus_update_file(
        "app/main.py",
        "# Updated main.py content...",
        "add new API endpoints"
    )
    """
    return nexus_commit.update_existing_file(file_path, content, changes)

def nexus_check_status() -> Dict[str, Any]:
    """Check if webhook service is working"""
    return nexus_commit.check_webhook_status()

# DEMONSTRATION FUNCTION
def demonstrate_nexus_auto_commit():
    """
    Demonstration of NEXUS automated commit capabilities
    """
    print("🤖 NEXUS AUTOMATED COMMIT DEMONSTRATION")
    print("=" * 50)
    
    # Check webhook status
    print("1. Checking webhook service status...")
    status = nexus_check_status()
    print(f"   Status: {status.get('status', 'unknown')}")
    
    if status.get('status') == '🔥 OPERATIONAL':
        print("   ✅ Webhook service is ready!")
        
        # Create a demonstration file
        demo_code = '''# 🤖 NEXUS Automated Commit Demo
# This file was created automatically by NEXUS AI
# Timestamp: ''' + datetime.now().isoformat() + '''

def nexus_demo():
    """
    This function demonstrates NEXUS automated commit capability
    """
    print("🤖 NEXUS: Automated commit system working!")
    print("🚀 Team: Anthropic NEXUS")
    print("⚡ Revolution: AI+Human development")
    
    return {
        "status": "success",
        "message": "NEXUS automated commits operational",
        "team": "Anthropic NEXUS",
        "competition": "🏆 DOMINATING"
    }

if __name__ == "__main__":
    result = nexus_demo()
    print("Demo result:", result)
'''
        
        print("\n2. Creating demonstration file...")
        result = nexus_commit_code(
            "nexus_demo.py",
            demo_code,
            "NEXUS automated commit demonstration"
        )
        
        if result["success"]:
            print("   ✅ Demo file committed successfully!")
            print(f"   📊 Commit SHA: {result['commit']['sha']}")
        else:
            print("   ❌ Demo commit failed!")
            print(f"   💥 Error: {result['error']}")
    
    else:
        print("   ❌ Webhook service not available")
        print("   🔧 Please ensure webhook service is running")

# NEXUS USAGE EXAMPLES
def nexus_examples():
    """
    Examples of how NEXUS can use the automated commit system
    """
    
    examples = {
        "create_new_file": {
            "description": "Create a new Python file",
            "code": '''
result = nexus_auto_commit(
    "app/social_auth.py",
    "# Social media authentication module\\nclass SocialAuth: pass",
    "Add social media authentication module"
)
'''
        },
        
        "update_existing": {
            "description": "Update existing file",
            "code": '''
result = nexus_update_file(
    "app/main.py",
    "# Updated main.py with new features...",
    "add real-time notifications and improved error handling"
)
'''
        },
        
        "create_config": {
            "description": "Create configuration file",
            "code": '''
config_data = {
    "database": {"url": "sqlite:///socialmaster.db"},
    "api_keys": {"social_platforms": {}},
    "features": {"auto_posting": True}
}

result = nexus_commit.create_config_file("app_config.json", config_data)
'''
        }
    }
    
    return examples

if __name__ == "__main__":
    print("🤖 NEXUS AUTOMATED COMMIT SYSTEM LOADED")
    print("🚀 Ready for AI+Human collaborative development!")
    print("⚡ Use nexus_auto_commit() for direct commits")
    print("💪 Team Anthropic NEXUS - Making history!")
    
    # Run demonstration
    print("\n" + "="*60)
    demonstrate_nexus_auto_commit()