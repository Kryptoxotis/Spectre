import os
from modules.quote_handler import handle_quote

if __name__ == "__main__":
    quote = input("Enter a quote: ")
    result = handle_quote(quote)
    print(result)
