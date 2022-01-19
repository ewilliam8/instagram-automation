from .unfollow_util import get_actual_user_followers

def get_actual_followers(self, target_account):
    try:
        ret = get_actual_user_followers(
            self.browser,
            target_account,
            self.logger,
        )

    except (TypeError, RuntimeWarning) as err:
        print(err)
        ret = None
    
    return ret