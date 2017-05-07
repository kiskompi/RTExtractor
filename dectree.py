class DecTree:
    """
    This is a placeholder decision tree for representative purposes so RTClassifier can
    temporarily work it. The tree only works on twitter page elements and only for
    demonstrative purposes Gets a feature vector. Based on the given vector it classifies
    the element to one of the following groups:
    * INNER
    * OUTER
    * REVEAL
    * MISC
    """
    def __init__(self):
        pass

    @classmethod
    def classify(cls, features: list) -> str:
        """
        This function returns the type of an element based on a given feature vector
        :type features: dict
        :param features: the extracted feature vector of the element (HTML attributes)
        :return: the type of the link as str
        """
        if ("js-stream-item" in features and "stream-item" in features
            or "new-tweets-bar" in features and "js-new-tweets-bar" in features
            or 'QuoteTweet-link' in features and 'js-nav' in features
            or "tweet" in features and " js-actionable-tweet" in features and "has-content" in features):
                return "REVEAL"
        elif ("js-display-url" in features
                or "TwitterCard-container" in features and "TwitterCard-container--clickable" in features
                and "SummaryCard--small" in features and "PlayerCard--preview" in features):
            return "OUTER"
        elif ("fullname" in features and "show-popup-with-id"
              or "twitter-hashtag" in features and "pretty-link" in features and "js-nav" in features
              or "trend-item" in features and "js-trend-item " in features and "context-trend-item" in features):
            return "INNER"
        elif ("modal-btn" in features and "modal-close" in features and "js-close" in features
            or "Icon" in features and "Icon--close" in features and "Icon--large" in features):
            return "CLOSE"

        # REVEAL:
        # ha a href = "#"
        # ha a  class = js-stream-item stream-item stream-item
        # ha class = new-tweets-bar js-new-tweets-bar
        # QuoteTweet-link js-nav

        # OUTER:
        # class = js-display-url

        # INNER:
        # class = fullname show-popup-with-id
        # class = twitter-hashtag pretty-link js-nav
        # class = trend-item js-trend-item  context-trend-item

