import Head from 'next/head'
import styles from '../styles/Home.module.css'
import { useShowsQuery, getShows } from '../hooks/queries/shows';
import { dehydrate, QueryClient} from 'react-query';

export async function getServerSideProps() {
  const queryClient = new QueryClient()

  await queryClient.prefetchQuery('shows', getShows)

  return {
    props: {
      dehydratedState: dehydrate(queryClient),
    },
  }
}

export default function Home() {
  const shows = useShowsQuery();

  if (!shows){
    return;
  } else{
    const content = shows.map((show) =>
    <div key={show.id}>
      <h3>{show.showName}</h3>
      <p>{show.desc}</p>
    </div>
  );
  }

  return (
    <>
      <Head>
        <title>Community Podcast</title>
        <meta name="description" content="Generated by create next app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main>
        <h1>Community Podcast</h1>
        {shows.map((show) =>
        <>
          <h2>{show.showName}</h2>
          <p>{show.desc}</p>
        </>
      )}
      
      </main>
    </>
  )
}
