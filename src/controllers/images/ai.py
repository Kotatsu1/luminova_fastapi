from dotenv import load_dotenv
import replicate

load_dotenv()



def image_caption(image_url):
    caption = replicate.run(
            "salesforce/blip:2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746",
            input={"image": image_url},
        )
    return caption


def image_generation(prompt: str):
    try:
        output_url = replicate.run(
            "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
            input={"prompt": prompt}
        )
        return output_url[0]
    except:
        return 'Probably NSFW request'