# Tracks who can see shared ride data
# Stores set of approved friends into owner_id
_APPROVED_FRIENDS = {}

# Add a friend to approved list
def add_approved_friend(owner_id, friend_id):
    if owner_id not in _APPROVED_FRIENDS:
        _APPROVED_FRIENDS[owner_id] = set()
    _APPROVED_FRIENDS[owner_id].add(friend_id)

# Remove from approved list
def remove_approved_friend(owner_id, friend_id):
    if owner_id in _APPROVED_FRIENDS:
        _APPROVED_FRIENDS[owner_id].discard(friend_id)

# Get a copy of all approved friends
def get_approved_friends(owner_id):
    return _APPROVED_FRIENDS.get(owner_id, set()).copy()

# Check if viewer is in approved list
def is_approved_friend(owner_id, viewer_id):
    return viewer_id in _APPROVED_FRIENDS.get(owner_id, set())

# Check if viewer is allowed to see shared data
def can_view_shared_data(owner_id, viewer_id, extra_allowed=None):
    if owner_id == viewer_id:
        return True

    allowed = set(_APPROVED_FRIENDS.get(owner_id, set()))

    # Temporary access for single id or list of ids
    if extra_allowed:
        if isinstance(extra_allowed, (str, int)):
            extra_allowed = [extra_allowed]
        allowed.update(extra_allowed)

    return viewer_id in allowed