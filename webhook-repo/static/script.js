function formatEvent(event) {
  const time = new Date(event.timestamp).toUTCString();
  if (event.action === 'push') {
    return `${event.author} pushed to ${event.to_branch} on ${time}`;
  } else if (event.action === 'pull_request') {
    return `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${time}`;
  }
  return '';
}

async function fetchEvents() {
  const res = await fetch('/get_events');
  const data = await res.json();
  const list = document.getElementById('event-list');
  list.innerHTML = '';
  data.forEach(event => {
    const li = document.createElement('li');
    li.textContent = formatEvent(event);
    list.appendChild(li);
  });
}

setInterval(fetchEvents, 15000); // Poll every 15 seconds
fetchEvents();
