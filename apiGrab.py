import yaml

from main import apiRun

# May 9, 2024
# "" if wanting todays date
date = ""

calories = apiRun("calories", date)
distance = apiRun("distance", date)
time = apiRun("time", date)


# load yaml
with open("_config.yml") as file_in:
  config = yaml.load(file_in, Loader=yaml.FullLoader)

config['rowing_calories'] = calories
config['rowing_distance'] = distance
config['rowing_time'] = time

with open("_config.yml", "w") as file_out:
  yaml.dump(config, file_out, default_flow_style=False, sort_keys=False)