from db_logic import Session

sesh = Session()

def main() -> None:
    print(f"Main running.\n")
    print(f"Attempting to start Greptile AI bot session...")
    sesh.run()

if __name__ == "__main__":
    main()
