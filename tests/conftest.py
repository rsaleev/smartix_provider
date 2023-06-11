from smartix_provider.hooks.smartix_hook import SmartixHook


def get_client():
    hook = SmartixHook()
    yield hook