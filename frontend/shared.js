// shared.js — utilities used across tool pages

// Download helper: accepts Blob or ArrayBuffer
function downloadFile(data, filename, mime) {
  const blob = data instanceof Blob ? data : new Blob([data], { type: mime || 'application/octet-stream' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

// simple POST file helper (backend conversion)
async function postFileToServer(url, file, fieldName = 'file') {
  const fd = new FormData();
  fd.append(fieldName, file);
  const resp = await fetch(url, { method: 'POST', body: fd });
  if (!resp.ok) throw new Error('Server conversion failed: ' + resp.statusText);
  return resp.blob();
}

// small UX utility for disabling button while busy
function setBusy(btn, isBusy, textWhileBusy = 'Processing...') {
  if (!btn) return;
  if (isBusy) {
    btn.dataset.old = btn.innerHTML;
    btn.innerHTML = textWhileBusy;
    btn.disabled = true;
  } else {
    btn.innerHTML = btn.dataset.old || btn.innerHTML;
    btn.disabled = false;
  }
}
