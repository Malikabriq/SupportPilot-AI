import { useRouter } from 'next/router';
import Head from 'next/head';

export default function TicketDetail() {
    const router = useRouter();
    const { id } = router.query;

    return (
        <div className="container mx-auto p-4">
            <Head>
                <title>Ticket {id} - SupportPilot AI</title>
            </Head>
            <h1 className="text-2xl font-bold">Ticket Details: {id}</h1>
            <p>Loading details...</p>
        </div>
    );
}
