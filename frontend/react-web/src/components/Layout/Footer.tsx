export const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white mt-auto">
      <div className="container mx-auto px-4 py-6">
        <p className="text-center text-sm">
          © {new Date().getFullYear()} Organic Store Search. Data from Jaivik Bharat (FSSAI).
        </p>
      </div>
    </footer>
  );
};
