from utils.mysql_utils import truncate_table

def truncate_user_behavior():
    truncate_table("user_behavior")
    print("user_behavior table truncated")

if __name__ == "__main__":
    truncate_user_behavior()