#!/usr/bin/env python3
"""Deploy GHL Agent to LangGraph Cloud"""

import argparse
import subprocess
import sys
import os
import json
from pathlib import Path

def check_requirements():
    """Check if required tools are installed"""
    print("🔍 Checking requirements...")
    
    # Check for langgraph CLI
    result = subprocess.run(["langgraph", "--version"], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ langgraph CLI not found. Install with: pip install -U langgraph-cli")
        return False
    print(f"✅ LangGraph CLI: {result.stdout.strip()}")
    
    # Check for git
    result = subprocess.run(["git", "--version"], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ git not found. Please install git.")
        return False
    print(f"✅ Git: {result.stdout.strip()}")
    
    return True

def validate_config():
    """Validate configuration files"""
    print("\n📋 Validating configuration...")
    
    # Check langgraph.json
    if not Path("langgraph.json").exists():
        print("❌ langgraph.json not found")
        return False
    
    try:
        with open("langgraph.json", "r") as f:
            config = json.load(f)
        print("✅ langgraph.json is valid")
    except json.JSONDecodeError as e:
        print(f"❌ langgraph.json is invalid: {e}")
        return False
    
    # Check .env file
    if not Path(".env").exists():
        print("⚠️  .env file not found. Make sure to set environment variables in deployment.")
    else:
        print("✅ .env file found")
    
    # Check required files
    required_files = [
        "ghl_agent/agent/graph.py",
        "ghl_agent/config.yaml",
        "pyproject.toml"
    ]
    
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ Required file not found: {file}")
            return False
        print(f"✅ {file} found")
    
    return True

def check_env_vars():
    """Check required environment variables"""
    print("\n🔐 Checking environment variables...")
    
    required_vars = [
        "LANGSMITH_API_KEY",
        "GHL_API_KEY",
        "GHL_LOCATION_ID",
        "GHL_CALENDAR_ID"
    ]
    
    optional_vars = [
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "META_VERIFY_TOKEN",
        "META_APP_SECRET"
    ]
    
    missing_required = []
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            print(f"❌ {var} is not set")
            missing_required.append(var)
    
    for var in optional_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            print(f"⚠️  {var} is not set (optional)")
    
    return len(missing_required) == 0

def deploy_to_cloud(args):
    """Deploy to LangGraph Cloud"""
    print("\n🚀 Deploying to LangGraph Cloud...")
    
    # Build deployment command
    cmd = ["langgraph", "deploy"]
    
    if args.name:
        cmd.extend(["--name", args.name])
    else:
        cmd.extend(["--name", "ghl-customer-agent"])
    
    if args.github_repo:
        cmd.extend(["--github-repo", args.github_repo])
    
    if args.branch:
        cmd.extend(["--branch", args.branch])
    
    if args.api_key:
        cmd.extend(["--api-key", args.api_key])
    
    print(f"\nRunning: {' '.join(cmd)}")
    
    # Execute deployment
    result = subprocess.run(cmd, text=True)
    
    if result.returncode == 0:
        print("\n✅ Deployment successful!")
        print("\n📝 Next steps:")
        print("1. Check deployment status in LangSmith UI")
        print("2. Configure environment variables in deployment settings")
        print("3. Test the deployment with test_deployment.py")
        print("4. Set up webhooks to point to deployment URL")
    else:
        print("\n❌ Deployment failed!")
        sys.exit(1)

def deploy_local(args):
    """Deploy locally for testing"""
    print("\n🏠 Starting local deployment...")
    
    cmd = ["langgraph", "dev"]
    
    if args.port:
        cmd.extend(["--port", str(args.port)])
    
    print(f"\nRunning: {' '.join(cmd)}")
    print("\n📝 Local deployment will start at http://localhost:2024")
    print("Press Ctrl+C to stop\n")
    
    # Execute local deployment
    subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(description="Deploy GHL Agent")
    parser.add_argument("--mode", choices=["cloud", "local"], default="local",
                        help="Deployment mode (default: local)")
    parser.add_argument("--name", help="Deployment name (cloud mode)")
    parser.add_argument("--github-repo", help="GitHub repository (cloud mode)")
    parser.add_argument("--branch", default="main", help="Git branch (cloud mode)")
    parser.add_argument("--api-key", help="LangSmith API key (cloud mode)")
    parser.add_argument("--port", type=int, default=2024, help="Local port (local mode)")
    parser.add_argument("--skip-checks", action="store_true", help="Skip validation checks")
    
    args = parser.parse_args()
    
    print("🤖 GHL Agent Deployment Script")
    print("=" * 40)
    
    if not args.skip_checks:
        # Check requirements
        if not check_requirements():
            print("\n❌ Requirements check failed!")
            sys.exit(1)
        
        # Validate configuration
        if not validate_config():
            print("\n❌ Configuration validation failed!")
            sys.exit(1)
        
        # Check environment variables
        if args.mode == "cloud" and not check_env_vars():
            print("\n⚠️  Some required environment variables are missing!")
            print("Make sure to set them in the deployment settings.")
    
    # Deploy based on mode
    if args.mode == "cloud":
        deploy_to_cloud(args)
    else:
        deploy_local(args)

if __name__ == "__main__":
    main()