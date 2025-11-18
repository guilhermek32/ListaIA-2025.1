#!/usr/bin/env python
"""
Launcher script for the Wine Recommendation System
Run this from the project root directory
"""

import sys
from pathlib import Path

# Add backend to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Import and run the integrated system
from sistema_integrado import sistema_completo_com_justificativa

def main():
    """Main entry point"""
    print("🍷 Wine Recommendation System")
    print("=" * 80)
    
    # Example dishes to test
    pratos_exemplo = [
        "Sushi",
        "Filé ao molho madeira",
        "Salmão grelhado"
    ]
    
    print("\nTesting with example dishes...")
    print("To use LLM justifications, set PERPLEXITY_API_KEY in .env file\n")
    
    for prato in pratos_exemplo:
        try:
            sistema_completo_com_justificativa(prato, usar_llm=True)
            print("\n" + "=" * 80 + "\n")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            sys.exit(0)
        except Exception as e:
            print(f"Error processing {prato}: {e}")
            continue

if __name__ == "__main__":
    main()
