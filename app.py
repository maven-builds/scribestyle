from nicegui import ui, events # Import the ui and event classes from NiceGUI
import io # Import io (BytesIO) so the converter can handle uploaded files not yet in RAM
from PIL import Image # Handle image conversions
from pathlib import Path # Handle file names

ui.dark_mode(True) # Turn on dark mode
ui.image("ScribeStyle Logo.png").style("width: 615px; height: 215px; margin: 0 auto; display: block") # Load in the ScribeStyle logo
ui.label("An ad-free file converter, by Ebuka").style("font-size: 25px; margin: 0 auto; display: block; color: #38b6ff")
ui.label()
ui.label()

uploadType = ui.radio(["Text", "Images", "Audio", "Video"], value="Text").props("inline").style("font-size: 23px; margin: 0 auto; display: block") # Pick a file type
ui.label()
ui.label()

# Handle user uploads that are image

async def handleImageUploads(e: events.UploadEventArguments):
    ui.notify(f"You just uploaded {e.file.name}") # Notifiy the user of their upload
    rawImageUpload = await e.file.read() # Wait for an upload
    imageUpload = Image.open(io.BytesIO(rawImageUpload)) # Open the uploaded image
    imageUpload = imageUpload.convert("RGB") # Convert the image to a JPG-friendly color format

    jpgBuffer = io.BytesIO() # An output buffer for JPG files
    pngBuffer = io.BytesIO() # An output buffer for PNG files
    webpBuffer = io.BytesIO() # An output buffer for WEBP files
    svgBuffer = io.BytesIO() # An output buffer for SVG files
    gifBuffer = io.BytesIO() # An output buffer for GIF files

    # Save the converted image to the output buffer

    imageUpload.save(jpgBuffer, "JPEG") 
    imageUpload.save(pngBuffer, "PNG")
    imageUpload.save(webpBuffer, "WEBP")
    imageUpload.save(gifBuffer, "GIF")

    # Handle converted file names for different image formats

    originalFileName = Path(e.file.name).stem
    jpgFileName = f"{originalFileName}.jpg"
    pngFileName = f"{originalFileName}.png"
    webpFileName = f"{originalFileName}.webp"
    gifFileName = f"{originalFileName}.gif"

    ui.label()
    ui.label()

    # Different download options

    with ui.button_group():
        ui.button("Download JPG", on_click=lambda: ui.download.content(jpgBuffer.getvalue(), filename=jpgFileName)).style("color: #5170ff")
        ui.button("Download PNG", on_click=lambda: ui.download.content(pngBuffer.getvalue(), filename=pngFileName)).style("color: #5170ff")
        ui.button("Download WEBP", on_click=lambda: ui.download.content(webpBuffer.getvalue(), filename=webpFileName)).style("color: #5170ff")
        ui.button("Download GIF", on_click=lambda: ui.download.content(gifBuffer.getvalue(), filename=gifFileName)).style("color: #5170ff")

# Handle user uploads that are texts

async def handleTextUploads(e: events.UploadEventArguments):
    ui.notify(f"You just uploaded {e.file.name}")
    rawTextUpload = await e.file.read()


ui.upload(on_upload=handleImageUploads, auto_upload=True).props("accept=.png,.jpg,.webp,.gif").style("margin: 0 auto; display: block; background-color: #000000").bind_visibility_from(uploadType, "value", value="Images") # Handle images if the user picks that upload type
ui.upload(on_upload=handleTextUploads, auto_upload=True).props("accept=.docx,.pdf,.txt").style("margin: 0 auto; display: block; background-color: #000000").bind_visibility_from(uploadType, "value", value="Text") # Handle text uploads

ui.run() # Run the application