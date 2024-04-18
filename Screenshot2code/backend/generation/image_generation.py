import asyncio
import re
from typing import Dict, List, Union
from zhipuai import ZhipuAI
from bs4 import BeautifulSoup


async def process_tasks(model: str, prompts: List[str], api_key: str, base_url: str):
    tasks = [generate_image(model, prompt, api_key, base_url) for prompt in prompts]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    processed_results: List[Union[str, None]] = []
    for result in results:
        if isinstance(result, Exception):
            print(f"An exception occurred: {result}")
            processed_results.append(None)
        else:
            processed_results.append(result)  # type: ignore

    return processed_results


async def generate_image(model: str, prompt: str, api_key: str, base_url: str):
    client = ZhipuAI(api_key=api_key, base_url=base_url)
    image_params: Dict[str, Union[str, int]] = {
        "model": model,
        "prompt": prompt,
    }
    res = client.images.generations(**image_params)  # type: ignore
    client.close()
    return res.data[0].url


def extract_dimensions(url: str):
    # Regular expression to match numbers in the format '300x200'
    matches = re.findall(r"(\d+)x(\d+)", url)

    if matches:
        width, height = matches[0]  # Extract the first match
        width = int(width)
        height = int(height)
        return (width, height)
    else:
        return (100, 100)


async def generate_images(
        code: str, api_key: str, base_url: Union[str, None], model: str
):
    # Find all images
    soup = BeautifulSoup(code, "lxml")
    images = soup.find_all("img")

    # Extract alt texts as image prompts
    alts = []
    for img in images:
        # Only include URL if the image starts with https://placehold.co
        if img["src"].startswith("https://placehold.co"):
            alts.append(img.get("alt", None))  # type: ignore

    # Exclude images with no alt text
    alts = [alt for alt in alts if alt is not None]  # type: ignore

    # Remove duplicates
    prompts = list(set(alts))  # type: ignore

    # Return early if there are no images to replace
    if len(prompts) == 0:  # type: ignore
        return soup.prettify()
    # Generate images
    results = await process_tasks(model, prompts, api_key, base_url)  # type: ignore
    # Create a dict mapping alt text to image URL
    mapped_image_urls = dict(zip(prompts, results))  # type: ignore

    # Replace old image URLs with the generated URLs
    for img in images:
        # Skip images that don't start with https://placehold.co (leave them alone)
        if not img["src"].startswith("https://placehold.co"):
            continue

        new_url = mapped_image_urls[img.get("alt")]

        if new_url:
            # Set width and height attributes
            width, height = extract_dimensions(img["src"])
            img["width"] = width
            img["height"] = height
            # Replace img['src'] with the mapped image URL
            img["src"] = new_url
        else:
            width, height = extract_dimensions(img["src"])
            img["width"] = width
            img["height"] = height
            print("Image generation failed for alt text:" + img.get("alt"))

    # Return the modified HTML
    # (need to prettify it because BeautifulSoup messes up the formatting)
    return soup.prettify()
