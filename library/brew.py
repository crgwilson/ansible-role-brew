#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = """
"""

EXAMPLES = """
- name: "Install git-number"
  brew:
    name: git-number
    state: present

- name: "Install multiple packages"
  brew:
    name:
      - yadm
      - neovim
      - redis

- name: "Update brew packages"
  brew:
    update_cache: true

- name: "Upgrade all brew packages"
  brew:
    upgrade: true

- name: "Upgrade all brew packages using a non-standard path"
  brew:
    path: /opt/brew/bin/brew
    update: true
"""

RETURN = """
"""


def run_cmd(module, cmd):
    brew_path = module.params["path"]
    full_cmd = brew_path + " " + cmd

    (rc, out, err) = module.run_command(full_cmd, check_rc=True)
    if rc != 0:
        # TODO: When this fails stderr spits out a bunch of garbage that fills
        #       up the screen
        module.fail_json(
            msg="Error occurred when running command %s" % (cmd),
            stdout=out,
            stderr=err,
            rc=rc
        )


def run_update(module):
    subcommand = "update"
    run_cmd(module, subcommand)


def run_upgrade(module):
    subcommand = "upgrade"
    run_cmd(module, subcommand)


def run_install(module, package_name):
    subcommand = "install " + package_name
    run_cmd(module, subcommand)


def run_uninstall(module, package_name):
    subcommand = "uninstall " + package_name
    run_cmd(module, subcommand)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="list"),
            state=dict(default="present", choice=["present", "absent"]),
            path=dict(type="str", default="brew"),  # TODO: Fix this default
            update_cache=dict(type="bool", default=False),
            upgrade=dict(type="bool", default=False),
        ),
        supports_check_mode=True,
    )

    name = module.params["name"]
    state = module.params["state"]
    update_cache = module.params["update_cache"]
    upgrade = module.params["upgrade"]

    result = dict(changed=False, warnings=list())

    if update_cache:
        run_update(module)

    if upgrade:
        run_upgrade(module)

    if name:
        for package in name:
            if state == "absent":
                run_uninstall(module, package)
            else:
                run_install(module, package)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
