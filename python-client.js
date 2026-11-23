// Ponte entre a interface e o interpretador Python; não realiza a multiplicação.
export class PythonClient {
  constructor() {
    this.worker = new Worker(new URL('./python-worker.js', import.meta.url), {type: 'module'});
    this.pending = new Map();
    this.nextId = 0;
    this.ready = new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error('O carregamento do Python demorou demais. Atualize a página.')), 90000);
      this.worker.onmessage = ({data}) => {
        if (data.type === 'ready') {clearTimeout(timer); resolve(); return;}
        if (data.type === 'init-error') {clearTimeout(timer); reject(new Error('Não foi possível carregar o Python.')); return;}
        const job = this.pending.get(data.id);
        if (!job) return;
        this.pending.delete(data.id);
        data.ok ? job.resolve(data.dados) : job.reject(new Error(data.erro));
      };
      this.worker.onerror = () => {
        clearTimeout(timer);
        const error = new Error('Não foi possível carregar o Python. Atualize a página.');
        reject(error);
        for (const job of this.pending.values()) job.reject(error);
        this.pending.clear();
      };
    });
  }
  async calculate(a, b) {
    await this.ready;
    return new Promise((resolve, reject) => {
      const id = ++this.nextId;
      this.pending.set(id, {resolve, reject});
      this.worker.postMessage({id, json: JSON.stringify({a, b})});
    });
  }
}
