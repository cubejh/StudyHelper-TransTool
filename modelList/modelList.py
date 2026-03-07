from google import genai

client = genai.Client(api_key="AIzaSyCn4DTfqZFo0XwV3wMCCY2L2Ssx5iag0zI")

output_file = "model_list.txt"

with open(output_file, "w", encoding="utf-8") as f:
    header = "valid model list：\n" + "-" * 50 + "\n"
    print(header)
    f.write(header)

    for model in client.models.list():
        name = getattr(model, 'name', 'unknow')
        actions = getattr(model, 'supported_actions', 'not support details')

        text = (
            f"model ID: {name}\n"
            f"support: {actions}\n"
            f"details: {model}\n"
            + "-" * 50 + "\n"
        )

        #print(text)
        f.write(text)

print(f"write in {output_file}")