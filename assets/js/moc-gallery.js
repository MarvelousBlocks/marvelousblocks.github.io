(() => {
  const article = document.querySelector('.moc-article, .minifig-article');
  const dialog = document.querySelector('.moc-lightbox');
  if (!article || !dialog) return;

  // Benachbarte reine Bildabsätze zusammenfassen; Bauabschnitte bleiben erhalten.
  let gallery = null;
  for (const element of Array.from(article.children)) {
    const images = Array.from(element.children);
    const isPhotoParagraph = element.tagName === 'P' &&
      images.length > 0 && images.every(child => child.tagName === 'IMG') &&
      element.textContent.trim() === '';
    if (!isPhotoParagraph) {
      gallery = null;
      continue;
    }
    if (!gallery) {
      gallery = document.createElement('div');
      gallery.className = 'moc-gallery';
      article.insertBefore(gallery, element);
    }
    for (const image of images) {
      const link = document.createElement('a');
      link.href = image.src;
      link.setAttribute('aria-label', `Open photo: ${image.alt || 'MOC'}`);
      image.loading = 'lazy';
      image.decoding = 'async';
      link.append(image);
      gallery.append(link);
    }
    element.remove();
  }

  const links = Array.from(article.querySelectorAll('.moc-gallery a'));
  const preview = dialog.querySelector('.moc-lightbox-image');
  const counter = dialog.querySelector('.moc-lightbox-counter');
  const previous = dialog.querySelector('[data-previous]');
  const next = dialog.querySelector('[data-next]');
  let index = 0;
  let opener = null;

  const showPhoto = position => {
    index = (position + links.length) % links.length;
    preview.src = links[index].href;
    preview.alt = links[index].querySelector('img').alt;
    counter.textContent = `${index + 1} / ${links.length}`;
  };

  links.forEach((link, position) => {
    link.addEventListener('click', event => {
      // Links bleiben ohne Dialog-Unterstützung und für neue Tabs nutzbar.
      if (typeof dialog.showModal !== 'function' || event.ctrlKey ||
          event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      opener = link;
      showPhoto(position);
      dialog.showModal();
    });
  });

  previous.hidden = next.hidden = links.length < 2;
  previous.addEventListener('click', () => showPhoto(index - 1));
  next.addEventListener('click', () => showPhoto(index + 1));
  dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      showPhoto(index + (event.key === 'ArrowLeft' ? -1 : 1));
    }
  });
  dialog.addEventListener('click', event => {
    const bounds = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < bounds.left ||
        event.clientX > bounds.right || event.clientY < bounds.top ||
        event.clientY > bounds.bottom)) dialog.close();
  });
  dialog.addEventListener('close', () => {
    preview.removeAttribute('src');
    opener?.focus();
  });
})();
