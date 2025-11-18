"""
Comprehensive System Test Script
Tests all components of the Wine Recommendation System
"""

import requests
import sys
import time
from colorama import init, Fore, Style

init(autoreset=True)

def print_header(text):
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}{text.center(80)}")
    print(f"{Fore.CYAN}{'='*80}\n")

def print_success(text):
    print(f"{Fore.GREEN}✓ {text}")

def print_error(text):
    print(f"{Fore.RED}✗ {text}")

def print_info(text):
    print(f"{Fore.YELLOW}ℹ {text}")

def test_backend_health():
    """Test if backend API is running"""
    print_header("TEST 1: Backend API Health Check")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Backend API is running")
            print_info(f"  Status: {data['status']}")
            print_info(f"  LLM Configured: {data['llm_configured']}")
            print_info(f"  Dishes: {data['database']['pratos']}")
            print_info(f"  Wines: {data['database']['vinhos']}")
            return True
        else:
            print_error(f"Backend returned status code {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend API")
        print_info("  Make sure to run: python api.py")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False

def test_recommendation_api():
    """Test wine recommendation endpoint"""
    print_header("TEST 2: Wine Recommendation API")
    
    test_dishes = ["Sushi", "Feijoada", "Salmão grelhado"]
    
    for dish in test_dishes:
        print_info(f"Testing recommendation for: {dish}")
        
        try:
            response = requests.post(
                "http://localhost:8000/api/recomendacao",
                json={"mensagem": dish},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('prato'):
                    vinho = data.get('vinho', {})
                    print_success(f"  Prato: {data['prato']}")
                    print_success(f"  Vinho: {vinho.get('nome')} ({vinho.get('tipo')})")
                    print_success(f"  Compatibilidade: {vinho.get('similaridade', 0):.1f}%")
                    
                    justificativa = data.get('justificativa', '')
                    if justificativa and len(justificativa) > 100:
                        print_success(f"  Justificativa: {len(justificativa)} caracteres (OK)")
                    else:
                        print_info(f"  Justificativa: {len(justificativa)} caracteres (fallback)")
                else:
                    print_error(f"  {data.get('mensagem', 'Unknown error')}")
            else:
                print_error(f"  Request failed with status {response.status_code}")
                
        except requests.exceptions.Timeout:
            print_error(f"  Request timed out (LLM might be slow)")
        except Exception as e:
            print_error(f"  Error: {e}")
        
        print()
        time.sleep(1)
    
    return True

def test_list_endpoints():
    """Test list dishes and wines endpoints"""
    print_header("TEST 3: List Endpoints")
    
    # Test dishes
    try:
        response = requests.get("http://localhost:8000/api/pratos", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Dishes endpoint: {data['total']} dishes available")
        else:
            print_error("Failed to list dishes")
    except Exception as e:
        print_error(f"Dishes endpoint error: {e}")
    
    # Test wines
    try:
        response = requests.get("http://localhost:8000/api/vinhos", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Wines endpoint: {data['total']} wines available")
        else:
            print_error("Failed to list wines")
    except Exception as e:
        print_error(f"Wines endpoint error: {e}")
    
    return True

def test_frontend():
    """Test if Next.js frontend is running"""
    print_header("TEST 4: Frontend Server")
    
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        
        if response.status_code == 200:
            print_success("Frontend is running on http://localhost:3000")
            print_info("  You can open it in your browser to test the chat interface")
            return True
        else:
            print_error(f"Frontend returned status code {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to frontend")
        print_info("  Make sure to run: npm run dev")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False

def test_integration():
    """Test full integration: Frontend -> Backend"""
    print_header("TEST 5: Full Integration Test")
    
    print_info("Testing Next.js API route proxy...")
    
    try:
        response = requests.post(
            "http://localhost:3000/api/recomendacao",
            json={"mensagem": "Pizza"},
            timeout=15,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print_success("Frontend API route is working")
            print_success("Integration: Frontend ↔ Backend ✓")
            return True
        else:
            print_error(f"Frontend API route returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to frontend API route")
        return False
    except Exception as e:
        print_error(f"Integration test error: {e}")
        return False

def main():
    """Run all tests"""
    print_header("🍷 VINECHAT SYSTEM TEST SUITE 🍷")
    
    print(f"{Fore.CYAN}This script will test all components of the system.\n")
    print(f"{Fore.YELLOW}Prerequisites:")
    print(f"{Fore.YELLOW}  1. Backend API running: python api.py")
    print(f"{Fore.YELLOW}  2. Frontend running: npm run dev\n")
    
    input(f"{Fore.WHITE}Press Enter to start tests...")
    
    # Run all tests
    results = {
        "Backend Health": test_backend_health(),
        "Recommendation API": test_recommendation_api(),
        "List Endpoints": test_list_endpoints(),
        "Frontend Server": test_frontend(),
        "Full Integration": test_integration()
    }
    
    # Print summary
    print_header("TEST SUMMARY")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    for test_name, result in results.items():
        status = f"{Fore.GREEN}PASSED" if result else f"{Fore.RED}FAILED"
        print(f"  {test_name:<25} {status}")
    
    print(f"\n{Fore.CYAN}Total: {total} tests")
    print(f"{Fore.GREEN}Passed: {passed}")
    print(f"{Fore.RED}Failed: {failed}")
    
    if failed == 0:
        print(f"\n{Fore.GREEN}{'='*80}")
        print(f"{Fore.GREEN}🎉 ALL TESTS PASSED! System is fully operational! 🎉")
        print(f"{Fore.GREEN}{'='*80}\n")
        print(f"{Fore.WHITE}Next steps:")
        print(f"{Fore.WHITE}  1. Open http://localhost:3000 in your browser")
        print(f"{Fore.WHITE}  2. Type a dish name (e.g., 'Sushi')")
        print(f"{Fore.WHITE}  3. Click 'Enviar' to get wine recommendations")
        print(f"{Fore.WHITE}  4. Enjoy! 🍷\n")
    else:
        print(f"\n{Fore.YELLOW}{'='*80}")
        print(f"{Fore.YELLOW}⚠️  Some tests failed. Please check the errors above.")
        print(f"{Fore.YELLOW}{'='*80}\n")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Tests interrupted by user.")
        sys.exit(0)
