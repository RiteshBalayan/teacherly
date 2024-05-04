import React, { useState, useEffect } from 'react';

function TikTokContainer() {
    const [content, setContent] = useState(null);
    const [nextPage, setNextPage] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/tiktok-feed/');
                const data = await response.json();
                setContent(data.results[0]); 
                setNextPage(data.next); // 'next' is the key for next page URL in the API response
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, []);

    const fetchNextPage = async () => {
        try {
            const response = await fetch(nextPage);
            const data = await response.json();
            setContent(data.results[0]);
            setNextPage(data.next);
        } catch (error) {
            console.error('Error fetching next page:', error);
        }
    };

    const fetchPreviousPage = async () => {
        // You can implement fetching the previous page if needed
    };

    return (
        <div className="relative w-9/16 lg:w-2/3 h-screen bg-gray-200 border border-gray-300 rounded-md mx-auto mt-8 overflow-hidden">
            {content && (
                <div>
                    <h1 className="text-xl font-bold px-4 py-2">{content.title}</h1>
                    {/* Render the content based on its type */}
                    {content.content_type === 'video' && (
                        <video src={content.video_file} controls className="w-full h-auto" />
                    )}
                    {content.content_type === 'image' && (
                        <img src={content.image_file} alt={content.title} className="w-full h-auto" />
                    )}
                    {content.content_type === 'article' && (
                        <div className="p-4" dangerouslySetInnerHTML={{ __html: content.content }} />
                    )}
                </div>
            )}
            <div className="absolute bottom-0 w-full flex justify-evenly py-2">
                <button onClick={fetchPreviousPage} className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">Previous</button>
                <button onClick={fetchNextPage} className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">Next</button>
            </div>
        </div>
    );
}

export default TikTokContainer;


