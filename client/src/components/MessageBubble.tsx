import React from "react";

interface Message {
  id: string;
  content: string;
  sender: "user" | "assistant";
  timestamp: Date;
  table?: {  
    columns: string[];
    rows: string[][];
  };
}


interface MessageBubbleProps {
  message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.sender === "user";

  return (
    <div
      className={`flex ${
        isUser ? "justify-end" : "justify-start"
      } items-start space-x-3`}
    >
      {!isUser && (
        <img
          src="/images/main_logo.png"
          alt="Smart city Logo"
          className="h-10 w-auto"
        />
      )}

      <div
        className={`max-w-xs sm:max-w-md lg:max-w-lg xl:max-w-xl ${
          isUser ? "order-first" : ""
        }`}
      >
        <div
          className={`px-4 py-3 rounded-2xl ${
            isUser
              ? "bg-gray-100 text-grey rounded-br-md"
              : "bg-gray-100 text-gray-900 rounded-bl-md"
          }`}
        >
          <p className="text-sm sm:text-base leading-relaxed whitespace-pre-wrap break-words">
            {message.content}
          </p>
          
          {/* Render table if present */}
          {message.table && (
            <div className="mt-4">
              <div className="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-blue-50">
                      <tr>
                        {message.table.columns.map((column, index) => (
                          <th
                            key={index}
                            className="px-4 py-3 text-left text-xs font-semibold text-blue-700 uppercase tracking-wider"
                          >
                            {column}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {message.table.rows.map((row, rowIndex) => (
                        <tr key={rowIndex} className={rowIndex % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                                                  {row.map((cell, cellIndex) => (
                          <td
                            key={cellIndex}
                            className={`px-4 py-3 text-sm max-w-xs truncate ${
                              cell === 'NA' 
                                ? 'text-gray-400 italic' 
                                : 'text-gray-900'
                            }`}
                            title={cell}
                          >
                            {cell}
                          </td>
                        ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <div className="bg-gray-50 px-4 py-2 text-xs text-gray-500 border-t border-gray-200">
                  Showing {message.table.rows.length} record{message.table.rows.length !== 1 ? 's' : ''}
                </div>
              </div>
            </div>
          )}
        </div>

        <div
          className={`mt-1 text-xs text-gray-500 ${
            isUser ? "text-right" : "text-left"
          }`}
        ></div>
      </div>

      {isUser}
    </div>
  );
};

export default MessageBubble;
