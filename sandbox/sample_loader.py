import os

def load_sample(sample_dir):
    """
    Loads the first valid sample file from the given directory.

    Args:
        sample_dir (str): Path to sample directory.

    Returns:
        str or None: Full path to the sample file, or None if no valid samples found.
    """
    valid_ext = ('.py', '.exe', '.bat', '.sh')

    if not os.path.exists(sample_dir):
        # Sample directory does not exist
        return None

    try:
        samples = [f for f in os.listdir(sample_dir) if f.endswith(valid_ext) and os.path.isfile(os.path.join(sample_dir, f))]
    except Exception as e:
        # Could log the exception if logging is set up
        return None

    if samples:
        # Return full path to first valid sample
        return os.path.join(sample_dir, samples[0])

    return None
