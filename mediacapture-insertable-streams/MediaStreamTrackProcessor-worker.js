onmessage = async msg => {
  const reader = msg.data.readable.getReader();
  let doneValue = await reader.read();
  postMessage(doneValue.value);
  doneValue.value.close();
  // Continue reading until the stream is done due to a track.stop()
  while (true) {
    const doneValue = await reader.read();
    if (doneValue.done) {
      break;
    } else {
      doneValue.value.close();
    }
  }
  await reader.closed;
  postMessage('closed');
}
