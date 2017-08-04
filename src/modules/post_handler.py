"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        NetNeutralityBot
Date Created:       08/03/2017
Date Last Edited:   08/03/2017
Version:            v1.0
==========================================
"""

from src.modules.account import credentials


class PostHandler:

    # Edit subreddits here. Keep in mind, we probably shouldn't include subreddits like
    # /r/NetNeutrality, since they probably already know this information.
    subreddits = ['technology']
    search_terms = ['net neutrality']

    @staticmethod
    def find_matches(reddit, database):
        print('Finding posts that contain "Net Neutrality"')
        matches = []
        for subreddit in PostHandler.subreddits:
            posts = reddit.get_submissions(subreddit)
            for post in posts:
                for term in PostHandler.search_terms:
                    if term in post.title.lower():
                        if not database.match_exists(post.permalink):
                            matches.append((term, post))
        return matches

    @staticmethod
    def handle_matches(reddit, database, matches, message):
        for term, post in matches:
            print('Inserting record ' + post.permalink)
            database.insert_comment(post.permalink)
            comment = post.add_comment(message)
            database.commit()
            reddit.send_message(
                credentials['developer'],
                'Bot commented on post',
                '[Comment found here](' + comment.permalink + ')'
            )