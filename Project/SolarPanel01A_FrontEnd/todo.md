to include 

```js
function convertArrayOfObjectsToCSV(data) {
  const header = Object.keys(data[0]);
  const csv = [
    header.join(','),
    ...data.map((obj) => header.map((key) => obj[key]).join(','))
  ].join('\n');

  return csv;
}

function downloadCSV(data, filename) {
  const csv = convertArrayOfObjectsToCSV(data);
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = window.URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.style.display = 'none';
  a.href = url;
  a.download = filename;

  document.body.appendChild(a);
  a.click();

  window.URL.revokeObjectURL(url);
}
```