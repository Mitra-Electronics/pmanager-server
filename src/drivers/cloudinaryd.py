import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="dyq1mevvs",
    api_key="667459361613199",
    api_secret="6KGsJIlQbcGwU_irAEviB8fzYeQ",
    secure=True
)
CON = "https://res.cloudinary.com/dyq1mevvs/image/upload/"


def upload_img(file) -> str:
    data = cloudinary.uploader.upload(file)
    return cloudinary.CloudinaryImage(data["public_id"]).build_url()


def delete_img(url: str):
    cloudinary.uploader.destroy(url.replace(CON, ""))
