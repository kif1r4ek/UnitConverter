export function formatRelativeDate(isoString) {
    const date = new Date(isoString);
    const diff = Date.now() - date;

    const mins = Math.floor(diff / 60000);
    if (mins < 1) return 'Just now';
    if (mins < 60) return `${mins}m ago`;
    if (mins < 1440) return `${Math.floor(mins / 60)}h ago`;

    return date.toLocaleDateString();
}
