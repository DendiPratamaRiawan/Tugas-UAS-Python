from services.auth_service import AuthService
from services.admin_service import AdminService
from services.customer_service import CustomerService

def main():
    auth = AuthService()
    user = auth.login()
    if not user:
        return

    if user.role == "admin":
        AdminService().menu()
    else:
        CustomerService(user).menu()

if __name__ == "__main__":
    main()
