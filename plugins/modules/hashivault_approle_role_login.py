#!/usr/bin/env python

from ansible_collections.terryhowe.hashivault.plugins.module_utils.hashivault import hashivault_argspec
from ansible_collections.terryhowe.hashivault.plugins.module_utils.hashivault import hashivault_client
from ansible_collections.terryhowe.hashivault.plugins.module_utils.hashivault import hashivault_init
from ansible_collections.terryhowe.hashivault.plugins.module_utils.hashivault import hashiwrapper

ANSIBLE_METADATA = {'status': ['stableinterface'], 'supported_by': 'community', 'version': '1.1'}
DOCUMENTATION = '''
---
module: hashivault_approle_role_login
version_added: "4.0.0"
short_description: Hashicorp Vault approle role create token
description:
    - Create token for AppRole
options:
    state:
        description:
            - present
        default: present
    role_id:
        description:
            - AppRole RoleID
    secret_id:
        description:
            - AppRole SecretID
    mount_point:
        description:
            - mount point for role
        default: approle
    cidr_list:
        description:
            - Comma-separated string or list of CIDR blocks.
    metadata:
        description:
            - Metadata to be tied to the secret.
    wrap_ttl:
        description:
            - Wrap TTL.
extends_documentation_fragment: hashivault
'''
EXAMPLES = '''
---
- hosts: localhost
  tasks:
    - hashivault_approle_role_login:
        role_id: AAAA
        secret_id: AAAA
        state: present
      register: vault_approle_role_token
    - debug: msg="Role token id is {{vault_approle_role_secret_create.client_token}}"

'''


def main():
    argspec = hashivault_argspec()
    argspec['state'] = dict(required=False, choices=['present'], default='present')
    argspec['role_id'] = dict(required=True, type='str')
    argspec['secret_id'] = dict(required=True, type='str')
    argspec['cidr_list'] = dict(required=False, type='str')
    argspec['metadata'] = dict(required=False, type='dict')
    argspec['wrap_ttl'] = dict(required=False, type='str')
    argspec['secret'] = dict(required=False, type='str')
    module = hashivault_init(argspec, supports_check_mode=True)
    result = hashivault_approle_role_login(module)
    if result.get('failed'):
        module.fail_json(**result)
    else:
        module.exit_json(**result)


@hashiwrapper
def hashivault_approle_role_login(module):
    params = module.params
    state = params.get('state')
    role_id = params.get('role_id')
    secret_id = params.get('secret_id')
    try: 
        client = hashivault_client(params)
        
        response = client.auth.approle.login(
            secret_id=secret_id,
            role_id=role_id
        )

        return {'secret': response['auth'], 'response': response,'change': True, 'status': 'present'}
    except Exception as e:
        return {'failed': True, "msg": str(e)}


if __name__ == '__main__':
    main()
