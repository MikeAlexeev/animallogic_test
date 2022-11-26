#!/usr/bin/env python
import logging
from pathlib import Path

from user_manager.api import SystemConfiguration, UserManager


def run_example():
    system_configuration = SystemConfiguration([Path("./plugin_example")])
    user_manager = UserManager(system_configuration)

    # use default implementations now, later we will switch
    user_manager.output_users()
    user_manager.save_user(
        "user1",
        dataset_name="work",
        values={"address": "city1", "phone_number": "1234"},
    )

    user_manager.output_user("user1")

    user_manager.save_user(
        "user2",
        dataset_name="personal",
        values={"address": "city2", "phone_number": "5678"},
    )
    user_manager.save_user("user2", dataset_name="work", values={"address": "city2"})

    user_manager.search_users(username="user")
    user_manager.search_users(address="city2")

    # switching implementation
    system_configuration.set_output_implementation_name("json")
    user_manager.output_users()

    system_configuration.set_record_implementation_name("user-extended")
    user_manager.save_user(
        "user2", dataset_name="work", values={"email": "email@example.com"}
    )
    user_manager.output_users()

    user_manager.remove_user("user2", dataset_name="personal")
    user_manager.output_users()

    user_manager.remove_user("user1")
    user_manager.remove_user("user2")
    user_manager.output_users()


if __name__ == "__main__":
    print("\n--- starting example\n")
    logging.basicConfig(level=logging.INFO, format="-- %(message)s")
    run_example()
