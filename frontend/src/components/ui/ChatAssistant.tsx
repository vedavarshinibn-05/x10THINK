import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { chatWithAI } from '../../api/client';
import { useFarmStore } from '../../store/farmStore';

export default function ChatAssistant() {
  const [isOpen, setIsOpen] = useState(false);
  const [msgs, setMsgs] = useState<{role: 'user'|'ai', content: string}[]>([
    { role: 'ai', content: 'Hello! I am X10 AI, your farm intelligence assistant. What would you like to know about your land?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { analysisData } = useFarmStore();
  const endRef = useRef<HTMLDivElement>(null);

  const handleSend = async () => {
    if(!input.trim()) return;
    const q = input;
    setMsgs(prev => [...prev, {role: 'user', content: q}]);
    setInput('');
    setIsLoading(true);
    
    const reply = await chatWithAI(q, analysisData);
    setMsgs(prev => [...prev, {role: 'ai', content: reply}]);
    setIsLoading(false);
  };

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [msgs]);

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <AnimatePresence>
        {isOpen && (
          <motion.div 
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            className="mb-4 w-80 sm:w-96 h-[500px] glass flex flex-col overflow-hidden shadow-2xl"
          >
            <div className="p-4 border-b border-x10-border bg-black/40 flex justify-between items-center">
              <h3 className="font-bold text-x10-green flex items-center gap-2">
                <span className="relative flex h-3 w-3">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-x10-green opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-x10-green"></span>
                </span>
                X10 AI Assistant
              </h3>
              <button onClick={() => setIsOpen(false)} className="text-gray-400 hover:text-white">&times;</button>
            </div>
            
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {msgs.map((m, i) => (
                <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`p-3 rounded-xl max-w-[85%] text-sm ${m.role === 'user' ? 'bg-x10-green text-black rounded-br-none' : 'bg-black/50 border border-x10-border rounded-bl-none text-gray-200'}`}>
                    {m.content}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="p-3 rounded-xl bg-black/50 border border-x10-border rounded-bl-none text-gray-400 text-sm flex gap-1">
                    <span className="animate-bounce">.</span><span className="animate-bounce" style={{animationDelay:'0.2s'}}>.</span><span className="animate-bounce" style={{animationDelay:'0.4s'}}>.</span>
                  </div>
                </div>
              )}
              <div ref={endRef} />
            </div>
            
            <div className="p-3 border-t border-x10-border bg-black/40">
              <div className="flex gap-2">
                <input 
                  type="text" 
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && handleSend()}
                  placeholder="Ask about crops, soil, weather..."
                  className="flex-1 bg-black/50 border border-x10-border rounded px-3 py-2 text-sm focus:outline-none focus:border-x10-green text-white"
                />
                <button 
                  onClick={handleSend}
                  className="bg-x10-green text-black px-3 py-2 rounded font-bold hover:bg-green-400"
                >
                  &rarr;
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      
      {!isOpen && (
        <button 
          onClick={() => setIsOpen(true)}
          className="w-14 h-14 bg-x10-green rounded-full shadow-glow-green flex items-center justify-center text-black hover:scale-110 transition-transform"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path></svg>
        </button>
      )}
    </div>
  );
}
