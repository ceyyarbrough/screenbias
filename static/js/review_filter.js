// JS profanity and URL filter for review submission
const foulWords = [
  'fuck', 'shit', 'bitch', 'asshole', 'bastard', 'dick', 'pussy', 'cunt', 'cock', 'fag', 'slut', 'whore', 'nigger', 'retard', 'faggot', 'motherfucker', 'twat', 'douche', 'crap', 'bollocks', 'wanker', 'prick', 'arse', 'bugger', 'damn', 'hell', 'suck', 'jerk', 'tit', 'cum', 'spunk', 'piss', 'shag', 'tosser', 'arsehole', 'minge', 'knob', 'bellend', 'git', 'twat', 'shite', 'wank', 'shithead', 'shitface', 'douchebag', 'dipshit', 'dickhead', 'dildo', 'jackass', 'piss off', 'sod off', 'son of a bitch', 'bloody', 'prat', 'pillock', 'plonker', 'numpty', 'muppet', 'berk', 'div', 'nonce', 'slag', 'skank', 'scrubber', 'tart', 'tramp', 'trollop', 'slapper', 'sket', 'gash', 'gimp', 'goon', 'mong', 'minger', 'munter', 'nob', 'spaz', 'spunk', 'tart', 'tosser', 'tramp', 'trollop', 'twat', 'wank', 'wanker', 'whore', 'wuss'
];
const foulPattern = new RegExp('\\b(' + foulWords.map(w => w.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&')).join('|') + ')\\b', 'i');
const urlPattern = /(https?:\/\/|www\.|[a-zA-Z0-9\-]+\.(com|net|org|io|gov|edu|co|us|uk|ca|de|jp|fr|au|ru|ch|it|nl|se|no|es|mil|biz|info|mobi|name|aero|jobs|museum))/i;

document.addEventListener('DOMContentLoaded', function() {
  const reviewModal = document.getElementById('reviewModal');
  if (!reviewModal) return;
  const form = reviewModal.querySelector('form');
  const textarea = form.querySelector('textarea[name="review_text"]');
  const submitBtn = form.querySelector('button[type="submit"]');
  const errorDiv = document.createElement('div');
  errorDiv.className = 'alert alert-danger mt-2';
  errorDiv.style.display = 'none';
  form.querySelector('.modal-body').appendChild(errorDiv);

  function validateReview() {
    const text = textarea.value;
    if (!text.trim()) {
      errorDiv.style.display = 'none';
      submitBtn.disabled = true;
      return;
    }
    if (foulPattern.test(text)) {
      errorDiv.textContent = 'Profanity is not allowed in reviews.';
      errorDiv.style.display = 'block';
      submitBtn.disabled = true;
    } else if (urlPattern.test(text)) {
      errorDiv.textContent = 'URLs are not allowed in reviews.';
      errorDiv.style.display = 'block';
      submitBtn.disabled = true;
    } else {
      errorDiv.style.display = 'none';
      submitBtn.disabled = false;
    }
  }

  textarea.addEventListener('input', validateReview);
  validateReview();
});
