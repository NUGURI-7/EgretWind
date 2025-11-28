interface Article {
    id: number;
    title: string;
    content: string;
    author: {
        id: number;
        username: string;
    };
    status: 'draft' | 'published';
    publishedAt: string | null;
}

export type { Article }