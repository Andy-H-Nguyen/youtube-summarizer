import { Head, Html, Main, NextScript } from "next/document";

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        <meta
          name="YoutubeSummarizer - Transcibe Videos easily"
          content="YoutubeSummarizer - Transcibe Videos easily"
          about="YoutubeSummarizer - Transcibe Videos easily"
        />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <body className="body-bg">
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
