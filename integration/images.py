# from cri_api import AuthConfig
from cri_api.channel import Channel
from cri_api.images import Images

channel = Channel.from_env()
images = Images(channel)
print(images.list_images())
images.pull_image("busybox")
print(images.get_image("busybox"))
print("*" * 70)
[print(f"{i.repo_tags} -> {i.repo_digests} / {i.id}") for i in images.list_images()]
print("*" * 70)
busybox_images = [i.id for i in images.list_images() if any("busybox" in r for r in i.repo_tags)]
print(f"busybox images: {busybox_images}")
print("*" * 70)
[images.remove_image(i) for i in busybox_images]
[print(f"{i.repo_tags} -> {i.repo_digests} / {i.id}") for i in images.list_images()]
print("*" * 70)
# images.pull_image("busybox")
# images.pull_image("a-private-image", auth_config=AuthConfig(username="", password=""))
