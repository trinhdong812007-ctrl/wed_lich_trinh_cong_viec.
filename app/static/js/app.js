function updateClock() {
  const now = new Date();
  const clockEl = document.getElementById("clockNow");
  const dateEl = document.getElementById("dateNow");
  if (clockEl) {
    clockEl.textContent = now.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  }
  if (dateEl) {
    const days = ["Chu nhat","Thu hai","Thu ba","Thu tu","Thu nam","Thu sau","Thu bay"];
    const d = String(now.getDate()).padStart(2,'0');
    const m = String(now.getMonth()+1).padStart(2,'0');
    dateEl.textContent = `${days[now.getDay()]}, ${d}/${m}/${now.getFullYear()}`;
  }
}
setInterval(updateClock, 1000);
updateClock();

let schedulerLastUpdate = null;

async function fetchLastUpdate() {
  try {
    const response = await fetch('/api/last-update', { cache: 'no-store' });
    if (!response.ok) {
      return null;
    }
    const data = await response.json();
    return data.last_update;
  } catch (err) {
    return null;
  }
}

async function checkLiveUpdate() {
  const newUpdate = await fetchLastUpdate();
  if (!newUpdate) {
    return;
  }

  if (!schedulerLastUpdate) {
    schedulerLastUpdate = newUpdate;
    return;
  }

  if (newUpdate !== schedulerLastUpdate) {
    schedulerLastUpdate = newUpdate;
    if (document.hidden) {
      window.addEventListener('visibilitychange', function onVisible() {
        if (!document.hidden) {
          window.location.reload();
          window.removeEventListener('visibilitychange', onVisible);
        }
      });
    } else {
      window.location.reload();
    }
  }
}

setTimeout(checkLiveUpdate, 500);
setInterval(checkLiveUpdate, 10000);

const hamburgerBtn = document.getElementById("hamburgerBtn");
if (hamburgerBtn) {
  hamburgerBtn.addEventListener("click", () => {
    document.getElementById("sidebar").classList.toggle("open");
  });
}

function initMultiSelect(containerEl, options, { selected = [], placeholder = "Tim kiem...", name = "", onChange = null, positionMode = false, levelList = [] } = {}) {
  if (!containerEl) return;
  const hiddenInput = containerEl.querySelector('input[type="hidden"]');
  const wrapper = document.createElement('div');
  wrapper.className = 'multi-select-wrapper';

  const inputDiv = document.createElement('div');
  inputDiv.className = 'multi-select-input';

  const chipsSpan = document.createElement('span');
  chipsSpan.className = 'multi-select-chips';
  chipsSpan.style.display = 'contents';

  const searchInput = document.createElement('input');
  searchInput.type = 'text';
  searchInput.className = 'multi-select-search';
  searchInput.placeholder = placeholder;
  searchInput.autocomplete = 'off';

  inputDiv.appendChild(chipsSpan);
  inputDiv.appendChild(searchInput);

  const dropdown = document.createElement('div');
  dropdown.className = 'multi-select-dropdown';

  wrapper.appendChild(inputDiv);
  wrapper.appendChild(dropdown);

  if (hiddenInput) {
    hiddenInput.parentNode.insertBefore(wrapper, hiddenInput);
    wrapper.appendChild(hiddenInput);
  } else {
    const newHidden = document.createElement('input');
    newHidden.type = 'hidden';
    if (name) newHidden.name = name;
    wrapper.appendChild(newHidden);
    hiddenInput = newHidden;
  }

  const selectedSet = new Set(selected.filter(Boolean));
  let pendingPosition = null;

  function renderChips() {
    const values = Array.from(selectedSet);
    chipsSpan.innerHTML = values.map(v =>
      `<span class="multi-select-chip" data-value="${v}">${v}<span class="remove" data-value="${v}">&times;</span></span>`
    ).join('');
    if (hiddenInput) hiddenInput.value = values.join(', ');
    chipsSpan.querySelectorAll('.remove').forEach(el => {
      el.addEventListener('click', function(e) {
        e.stopPropagation();
        const val = this.dataset.value;
        selectedSet.delete(val);
        renderChips();
        renderDropdown(searchInput.value);
      });
    });
    if (onChange) onChange(Array.from(selectedSet));
  }

  function renderDropdown(filter) {
    if (positionMode && pendingPosition) {
      renderLevelOptions(pendingPosition);
      return;
    }
    const q = (filter || '').toLowerCase().trim();
    let filtered = options;
    if (q) {
      filtered = options.filter(o => o.toLowerCase().includes(q));
    }
    if (filtered.length === 0) {
      dropdown.innerHTML = '<div class="multi-select-no-results">Khong tim thay</div>';
      return;
    }
    dropdown.innerHTML = filtered.map(o => {
      const sel = selectedSet.has(o) ? 'selected' : '';
      return `<div class="multi-select-option ${sel}" data-value="${o}">
        <span class="toggle-icon">${selectedSet.has(o) ? '&#10003;' : ''}</span>
        <span>${o}</span>
      </div>`;
    }).join('');

    dropdown.querySelectorAll('.multi-select-option').forEach(el => {
      el.addEventListener('click', function(e) {
        e.stopPropagation();
        const val = this.dataset.value;
        if (positionMode) {
          pendingPosition = val;
          dropdown.classList.add('show');
          renderLevelOptions(val);
          return;
        }
        if (selectedSet.has(val)) {
          selectedSet.delete(val);
        } else {
          selectedSet.add(val);
        }
        renderChips();
        renderDropdown(searchInput.value);
        searchInput.focus();
      });
    });
  }

  function renderLevelOptions(position) {
    dropdown.classList.add('show');
    const prevPlaceholder = searchInput.placeholder;
    searchInput.placeholder = 'Chon trinh do cho ' + position + '...';
    dropdown.innerHTML = '<div class="multi-select-level-back" style="padding:6px 10px;cursor:pointer;color:#94a3b8;font-size:13px;border-bottom:1px solid #30363d;">&larr; Quay lai</div>' +
      levelList.map(level =>
        '<div class="multi-select-option" data-position="' + position + '" data-level="' + level + '">' +
          '<span>' + level + '</span>' +
        '</div>'
      ).join('');

    dropdown.querySelector('.multi-select-level-back').addEventListener('click', function(e) {
      e.stopPropagation();
      pendingPosition = null;
      searchInput.placeholder = prevPlaceholder;
      renderDropdown(searchInput.value);
    });

    dropdown.querySelectorAll('.multi-select-option').forEach(el => {
      el.addEventListener('click', function(e) {
        e.stopPropagation();
        const pos = this.dataset.position;
        const level = this.dataset.level;
        const combined = pos + '(' + level + ')';
        selectedSet.add(combined);
        pendingPosition = null;
        searchInput.placeholder = prevPlaceholder;
        renderChips();
        renderDropdown('');
        searchInput.focus();
      });
    });
  }

  searchInput.addEventListener('focus', () => {
    dropdown.classList.add('show');
    renderDropdown(searchInput.value);
  });

  searchInput.addEventListener('input', () => {
    dropdown.classList.add('show');
    renderDropdown(searchInput.value);
  });

  document.addEventListener('click', function closeDropdown(e) {
    if (!wrapper.contains(e.target)) {
      dropdown.classList.remove('show');
      if (pendingPosition) {
        pendingPosition = null;
        renderDropdown('');
      }
    }
  });

  searchInput.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      dropdown.classList.remove('show');
      if (pendingPosition) {
        pendingPosition = null;
        renderDropdown('');
      }
    }
  });

  renderChips();

  return {
    getValue: () => Array.from(selectedSet),
    setOptions: function(newOptions) {
      options = newOptions;
      renderDropdown(searchInput.value);
    },
    setSelected: function(values) {
      selectedSet.clear();
      values.filter(Boolean).forEach(v => selectedSet.add(v));
      renderChips();
      renderDropdown(searchInput.value);
    },
  };
}
