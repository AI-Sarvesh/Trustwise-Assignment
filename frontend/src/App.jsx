import { useState, useCallback } from 'react';
import TextInput from './components/TextInput';
import Results from './components/Results';

const App = () => {
  const [history, setHistory] = useState([]);

  // Use useCallback to prevent unnecessary re-renders
  const handleNewAnalysis = useCallback((updateFn) => {
    // If updateFn is a function, use it to update the state
    // This ensures we always have the latest state
    setHistory(typeof updateFn === 'function' ? updateFn : (prev) => [updateFn, ...prev]);
  }, []);

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Text Analysis Tool</h1>
      <TextInput onAnalyze={handleNewAnalysis} />
      <Results history={history} setHistory={setHistory} />
    </div>
  );
};

export default App;