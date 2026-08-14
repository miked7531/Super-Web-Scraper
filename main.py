import sys

def main():
    # sys.argv[0] is the script name itself
    # sys.argv[1:] are the actual arguments the user passed
    if len(sys.argv) < 2:
        # user forgot to give a url
        print("no website provided")
        sys.exit(1)

    if len(sys.argv) > 2:
        # user gave more than one extra argument
        print("too many arguments provided")
        sys.exit(1)
    
    # at this point there should be exactly one argument
    base_url = sys.argv[1]
    print(f"starting crawl of: {base_url}")

if __name__ == "__main__":
    main()
