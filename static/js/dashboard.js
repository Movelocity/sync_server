class DashboardManager {
  constructor() {
    this.clientListElement = document.getElementById('client-list');
    this.uploadBtn = document.getElementById('upload-btn');
    this.updateVersionBtn = document.getElementById('update-version-btn');
    this.fileListElement = document.getElementById('file-list');
    this.cachedFiles = [];
    this.tmpInput = null;

    this.initializeEventListeners();
    this.initializeClientUpdates();
  }

  /** 初始化事件监听器 */
  initializeEventListeners() {
    this.uploadBtn.onclick = () => this.selectFiles();
    this.updateVersionBtn.onclick = () => this.updateVersion();
  }

  /** 每隔30秒更新一次客户端列表 */
  initializeClientUpdates() {
    this.fetchClients();
    setInterval(() => this.fetchClients(), 30000);
  }

  /** 获取客户端列表 */
  async fetchClients() {
    try {
      const response = await fetch('/clients');
      const clients = await response.json();
      const now = new Date();

      this.clientListElement.innerHTML = '';
      for (const [client, data] of Object.entries(clients)) {
        const clientTime = new Date(data.last_seen);
        const li = document.createElement('li');
        li.classList.add('client-status', 'row-ex');
        
        // 创建备注编辑区域
        const noteSpan = document.createElement('span');
        noteSpan.classList.add('note-text');
        noteSpan.textContent = data.note || '点击添加备注';
        noteSpan.onclick = () => this.editNote(client, noteSpan, data.note);
        
        // 创建删除按钮
        const deleteBtn = document.createElement('i');
        deleteBtn.classList.add('material-icons', 'delete-btn');
        deleteBtn.textContent = 'delete';
        deleteBtn.onclick = () => this.deleteClient(client);
        
        li.innerHTML = `
          <div class="client-info">
            <span class="client-ip">${client}</span>
            <span class="last-seen">${data.last_seen.split('.')[0]}</span>
          </div>
        `;
        
        const controlsDiv = document.createElement('div');
        controlsDiv.classList.add('client-controls');
        controlsDiv.appendChild(noteSpan);
        controlsDiv.appendChild(deleteBtn);
        li.appendChild(controlsDiv);
        
        const timeDiff = (now - clientTime) / 1000 / 60;
        li.classList.add(timeDiff > 5 ? 'status-warning' : 'status-ok');
        this.clientListElement.appendChild(li);
      }
    } catch (error) {
      console.error('获取客户端信息失败:', error);
      M.toast({html: '获取客户端信息失败'});
    }
  }

  /** 更新文件列表 */
  updateFileListView() {
    this.fileListElement.innerHTML = '';
    this.cachedFiles.forEach((file, index) => {
      const li = document.createElement('li');
      li.classList.add('row-ex');
      li.innerHTML = `
        <span>${file.name}</span>
        <i class="material-icons remove-btn">close</i>
      `;
      
      li.querySelector('.remove-btn').onclick = () => {
        this.cachedFiles.splice(index, 1);
        this.updateFileListView();
      };
      
      this.fileListElement.appendChild(li);
    });
  }

  /** 选择文件 */
  selectFiles() {
    if(this.tmpInput) this.tmpInput.remove();
    this.tmpInput = document.createElement('input');
    this.tmpInput.style.position = 'fixed';
    this.tmpInput.style.opacity = 0;
    this.tmpInput.type = 'file';
    this.tmpInput.multiple = true;
    this.tmpInput.onchange = (event) => {
      const files = Array.from(event.target.files);
      if (files && files.length > 0) {
        this.cachedFiles.push(...files);
        this.updateFileListView();
      }
      this.tmpInput.remove();
      this.tmpInput = null;
    }
    document.body.appendChild(this.tmpInput);
    this.tmpInput.click();
  }

  /** 上传文件 */
  async postFiles() {
    if (this.cachedFiles.length === 0) {
      M.toast({html: '没有文件需要上传'});
      return false;
    }

    try {
      while (this.cachedFiles.length > 0) {
        const file = this.cachedFiles.pop();
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/upload', {
          method: 'POST',
          body: formData
        });
        const result = await response.text();
        console.log('上传 ' + file.name, result);
        this.updateFileListView();
      }
      return true;
    } catch (error) {
      console.error('文件上传失败:', error);
      M.toast({html: '文件上传失败'});
      return false;
    }
  }

  /** 更新版本 */
  async updateVersion() {
    try {
      const status_ok = await this.postFiles();
      if (!status_ok) return;

      const response = await fetch('/update_version');
      const result = await response.json();
      M.toast({html: `版本已更新: ${result.version}`});
      this.fetchClients();
    } catch (error) {
      console.error('版本更新失败:', error);
      M.toast({html: '版本更新失败'});
    }
  }

  /** 删除客户端 */
  async deleteClient(clientIp) {
    if (!confirm(`确定要删除客户端 ${clientIp} 吗？`)) {
      return;
    }
    
    try {
      const response = await fetch(`/client/${clientIp}`, {
        method: 'DELETE'
      });
      const result = await response.json();
      
      if (result.status === 'success') {
        M.toast({html: '客户端已删除'});
        this.fetchClients();
      } else {
        M.toast({html: '删除失败：' + result.message});
      }
    } catch (error) {
      console.error('删除客户端失败:', error);
      M.toast({html: '删除客户端失败'});
    }
  }

  /** 编辑备注 */
  async editNote(clientIp, noteElement, currentNote) {
    const newNote = prompt('请输入新的备注:', currentNote || '');
    if (newNote === null) return; // 用户取消
    
    try {
      const response = await fetch(`/client/${clientIp}/note`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ note: newNote })
      });
      
      const result = await response.json();
      if (result.status === 'success') {
        noteElement.textContent = newNote || '点击添加备注';
        M.toast({html: '备注已更新'});
      } else {
        M.toast({html: '更新备注失败：' + result.message});
      }
    } catch (error) {
      console.error('更新备注失败:', error);
      M.toast({html: '更新备注失败'});
    }
  }
}

// 初始化仪表板
document.addEventListener('DOMContentLoaded', () => {
  new DashboardManager();
});