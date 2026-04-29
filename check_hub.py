import langchainhub
try:
    p = langchainhub.pull("hwchase17/react")
    print("Success! The library is working, even if the IDE is showing red lines.")
except Exception as e:
    print(f"Actual Error: {e}")