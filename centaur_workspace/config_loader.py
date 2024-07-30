import yaml
import os


def load_agent_config(agent_name):
    config_path = os.path.join(
        "centaur_workspace", "config", "agents", f"{agent_name}.yaml"
    )
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    # Process tools
    if "tools" in config:
        config["tools"] = [{"name": tool} for tool in config["tools"]]

    return config
