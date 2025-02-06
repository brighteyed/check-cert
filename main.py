import ssl
import socket
from datetime import datetime, timedelta
import argparse
from colorama import Fore, Style, init

def get_cert_expiry_date(hostname, port=443):
    """Retrieve the SSL certificate expiration date for a given hostname."""
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                expiry_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                return expiry_date
    except (ssl.SSLError, socket.gaierror, ConnectionRefusedError) as e:
        print(Fore.RED + f"Error retrieving certificate for {hostname}: {e}" + Style.RESET_ALL)
        return None

def check_domains(file_path, warning_days):
    """Check SSL certificate expiration dates for domains in a file."""
    try:
        with open(file_path, 'r') as file:
            domains = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + f"File not found: {file_path}" + Style.RESET_ALL)
        return 1  # Return 1 for file not found error

    current_date = datetime.now()
    warning_found = False  # Flag to track if any warnings are found

    for domain in domains:
        expiry_date = get_cert_expiry_date(domain)
        if expiry_date:
            days_until_expiry = (expiry_date - current_date).days
            if days_until_expiry < warning_days:
                # Warning case: print "XX days" in red
                print(f"{domain}: {expiry_date.strftime('%Y-%m-%d')} (in {Fore.RED}{days_until_expiry} days{Style.RESET_ALL})")
                warning_found = True
            else:
                # Normal case: print "XX days" in green
                print(f"{domain}: {expiry_date.strftime('%Y-%m-%d')} (in {Fore.GREEN}{days_until_expiry} days{Style.RESET_ALL})")

    # Return 1 if any warnings were found, otherwise 0
    return 1 if warning_found else 0

def main():
    """Main function to parse arguments and check domain certificates."""
    # Initialize colorama for cross-platform support
    init()

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Check SSL certificate expiration dates for domains.")
    parser.add_argument("--file", type=str, default="domains.txt", help="Path to the file containing domains (one per line).")
    parser.add_argument("--days", type=int, default=45, help="Number of days to warn before certificate expiration.")
    args = parser.parse_args()

    # Check domains and exit with the appropriate status code
    exit_code = check_domains(args.file, args.days)
    exit(exit_code)

if __name__ == "__main__":
    main()