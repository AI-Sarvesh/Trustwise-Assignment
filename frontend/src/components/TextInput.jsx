import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

const TextInput = ({ onAnalyze }) => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to analyze text');
      }
      
      const analysisResult = await response.json();
      
      onAnalyze((prevHistory) => [analysisResult, ...prevHistory]);
      
      setText(''); // Clear the input after successful analysis
    } catch (error) {
      console.error('Error analyzing text:', error);
      setError(error.message || 'Failed to analyze text. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle>Text Analysis</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="w-full p-2 border rounded min-h-[100px]"
            placeholder="Enter text to analyze..."
            disabled={loading}
          />
          <div className="flex justify-between items-center">
            <button
              type="submit"
              disabled={loading || !text.trim()}
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
            >
              {loading ? 'Analyzing...' : 'Analyze'}
            </button>
            {loading && <span className="text-blue-500">Processing analysis...</span>}
          </div>
          {error && (
            <div className="text-red-500 mt-2">{error}</div>
          )}
        </form>
      </CardContent>
    </Card>
  );
};

export default TextInput;