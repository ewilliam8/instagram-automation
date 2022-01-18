from .unfollow_util import get_actual_user_followers

def get_actual_followers(self):
    try:
        get_actual_user_followers(
            self.browser,
            "mazayki",
            self.logger,
        )

    except (TypeError, RuntimeWarning) as err:
        print(err)