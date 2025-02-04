import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { Info } from 'lucide-react';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "./ui/tooltip";

const Results = ({ history, setHistory }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${import.meta.env.VITE_API_URL}/history`);
      if (!response.ok) {
        throw new Error('Failed to fetch history');
      }
      const data = await response.json();
      setHistory(data);
      setError(null);
    } catch (err) {
      console.error('Error fetching history:', err);
      setError('Failed to load analysis history');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const prepareHallucinationData = (data) => {
    return data.map((item, index) => ({
      name: index + 1,
      hallucination: parseFloat(item.hallucination_score.toFixed(2)),
    }));
  };

  const prepareEmotionData = (data) => {
    return data.map((item, index) => {
      const graphPoint = { name: index + 1 };
      Object.entries(item.emotion_scores || {}).forEach(([emotion, score]) => {
        graphPoint[emotion] = parseFloat((score * 100).toFixed(1));
      });
      return graphPoint;
    });
  };

  const HallucinationScoreInfo = () => (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger>
          <Info className="h-4 w-4 ml-2 inline-block" />
        </TooltipTrigger>
        <TooltipContent className="max-w-sm p-4">
          <div className="space-y-2">
            <p className="font-semibold">Understanding Hallucination Scores:</p>
            <ul className="list-disc pl-4 space-y-1">
              <li><span className="font-medium">0.8 - 1.0:</span> High reliability - Response is well-supported by context</li>
              <li><span className="font-medium">0.5 - 0.7:</span> Moderate reliability - Partial support or possible embellishments</li>
              <li><span className="font-medium">0.0 - 0.5:</span> Low reliability - Potential hallucinations or unsupported statements</li>
            </ul>
          </div>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );

  const EmotionScoreInfo = () => (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger>
          <Info className="h-4 w-4 ml-2 inline-block" />
        </TooltipTrigger>
        <TooltipContent className="max-w-sm p-4">
          <div className="space-y-2">
            <p className="font-semibold">Understanding Emotion Analysis:</p>
            <ul className="list-disc pl-4 space-y-1">
              <li>Shows the top emotions detected in the text</li>
              <li>Scores are shown as percentages (0-100%)</li>
              <li>Higher percentages indicate stronger emotional signals</li>
              <li>Multiple emotions may be present in a single text</li>
            </ul>
          </div>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );

  if (loading && !history.length) {
    return (
      <Card>
        <CardContent>
          <div className="text-center p-4">Loading results...</div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Analysis Overview Card */}
      <Card>
        <CardHeader>
          <CardTitle>Text Analysis Overview</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="prose max-w-none">
            <p className="text-gray-600">
              Our text analysis tool provides two main insights:
            </p>
            <div className="grid md:grid-cols-2 gap-4 mt-4">
              <div className="p-4 bg-gray-50 rounded-lg">
                <h3 className="font-semibold flex items-center">
                  Hallucination Detection
                  <HallucinationScoreInfo />
                </h3>
                <p className="text-sm mt-2">
                  Measures how well the text is grounded in reality and supported by evidence.
                  Scores range from 0 (completely unsupported) to 1 (fully supported).
                </p>
              </div>
              <div className="p-4 bg-gray-50 rounded-lg">
                <h3 className="font-semibold flex items-center">
                  Emotion Analysis
                  <EmotionScoreInfo />
                </h3>
                <p className="text-sm mt-2">
                  Identifies the emotional undertones in your text, showing the top 3 detected emotions
                  with their relative intensities as percentages.
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Two Graphs Container */}
      <div className="grid md:grid-cols-2 gap-4">
        {/* Hallucination Graph */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              Hallucination Scores
              <HallucinationScoreInfo />
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[400px]">
              <ResponsiveContainer>
                <LineChart data={prepareHallucinationData(history)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <RechartsTooltip />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="hallucination" 
                    stroke="#8884d8" 
                    name="Hallucination Score" 
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Emotion Graph */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              Emotion Scores
              <EmotionScoreInfo />
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[400px]">
              <ResponsiveContainer>
                <LineChart data={prepareEmotionData(history)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <RechartsTooltip />
                  <Legend />
                  {Object.keys(history[0]?.emotion_scores || {}).map((emotion, index) => (
                    <Line
                      key={emotion}
                      type="monotone"
                      dataKey={emotion}
                      stroke={`hsl(${index * 60}, 70%, 50%)`}
                      name={`${emotion}`}
                    />
                  ))}
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Results Table */}
      <Card>
        <CardHeader>
          <CardTitle>Analysis History</CardTitle>
        </CardHeader>
        <CardContent>
          {error ? (
            <div className="text-red-500">{error}</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead>
                  <tr>
                    <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      #
                    </th>
                    <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Time
                    </th>
                    <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Text
                    </th>
                    <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Hallucination Score (Vectara)
                    </th>
                    <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Top Emotions (Emotion)
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {history.map((item, index) => (
                    <tr key={item.id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {index + 1}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(item.created_at).toLocaleString()}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        {item.text}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {item.hallucination_score.toFixed(2)}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        <div className="space-y-1">
                          {Object.entries(item.emotion_scores || {})
                            .sort(([, a], [, b]) => b - a)
                            .map(([emotion, score], index) => (
                              <div key={index} className="flex justify-between">
                                <span className="font-medium">{emotion}:</span>
                                <span>{(score * 100).toFixed(1)}%</span>
                              </div>
                            ))}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Results;