path = r"C:\Users\Simran\Downloads\SchemeNavigator\SchemeNavigator\Scheme-Navigator-App-master\backend\agents\assistant_agent.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Fix the broken multiline f-strings
text = text.replace('खालीलप्रमाणे आहे:\n"]', 'खालीलप्रमाणे आहे:\\n"]')
text = text.replace('ఇక్కడ ఉన్నాయి:\n"]', 'ఇక్కడ ఉన్నాయి:\\n"]')
text = text.replace('வழிகாட்டுதல் இதோ:\n"]', 'வழிகாட்டுதல் இதோ:\\n"]')

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully fixed f-strings")
