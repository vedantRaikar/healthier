from openfoodfacts import API, APIVersion, Country, Environment, Flavor

api = API(
    user_agent="<application name>",
    username=None,
    password=None,
    country=Country.world,
    flavor=Flavor.off,
    version=APIVersion.v2,
    environment=Environment.org,
)

code = "3017620422003"
text = api.product.get(code)
results = api.product.text_search("pizza")
print(text)
