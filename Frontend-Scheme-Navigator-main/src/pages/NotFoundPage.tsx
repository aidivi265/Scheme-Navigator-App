import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Compass, Search, Home, ArrowRight, Sparkles, MapPin, AlertCircle } from 'lucide-react';
import { useTranslation } from '../hooks/useTranslation';

export const NotFoundPage: React.FC = () => {
  const { t, tp } = useTranslation();
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/explore?search=${encodeURIComponent(searchQuery.trim())}`);
    } else {
      navigate('/explore');
    }
  };

  return (
    <div className="min-h-[75vh] flex items-center justify-center px-4 py-12 sm:py-16 transition-colors">
      <div className="max-w-xl w-full bg-white dark:bg-slate-900 rounded-3xl p-8 sm:p-12 border border-slate-200 dark:border-slate-800 shadow-xl dark:shadow-none text-center space-y-7 relative overflow-hidden">
        {/* Top Glow */}
        <div className="absolute -top-20 left-1/2 -translate-x-1/2 w-64 h-64 bg-teal-400/15 dark:bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />

        {/* 404 Icon Badge */}
        <div className="relative mx-auto w-20 h-20 rounded-3xl bg-gradient-to-br from-teal-800 to-slate-950 p-2 shadow-xl border-2 border-teal-600/40 flex items-center justify-center">
          <Compass className="w-10 h-10 text-emerald-400 animate-spin-slow" />
          <span className="absolute -bottom-2 -right-2 px-2 py-0.5 bg-rose-500 text-white text-[10px] font-black rounded-full shadow-md">
            404
          </span>
        </div>

        {/* Heading & Subtitle */}
        <div className="space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-rose-50 dark:bg-rose-950/50 text-rose-700 dark:text-rose-300 text-xs font-bold border border-rose-200 dark:border-rose-900">
            <AlertCircle className="w-3.5 h-3.5" />
            <span>पृष्ठ उपलब्ध नहीं है (Page Not Found)</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            Lost Your Way in Welfare Navigation?
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 max-w-md mx-auto leading-relaxed">
            The page or scheme link you are looking for may have been moved, updated, or does not exist. Use the search below to find official schemes.
          </p>
        </div>

        {/* Direct Scheme Search Form */}
        <form onSubmit={handleSearchSubmit} className="relative max-w-md mx-auto">
          <Search className="w-4 h-4 text-slate-400 dark:text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search 4,700+ schemes (e.g. Kisan, Scholarship, Mudra)..."
            className="w-full pl-10 pr-24 py-3 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600 text-slate-800 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 rounded-2xl text-xs sm:text-sm font-medium outline-hidden focus:border-teal-600 focus:ring-2 focus:ring-teal-500/20 transition-all"
          />
          <button
            type="submit"
            className="absolute right-1.5 top-1/2 -translate-y-1/2 px-3 py-1.5 bg-teal-800 hover:bg-teal-900 text-white text-xs font-bold rounded-xl transition-all shadow-xs cursor-pointer"
          >
            Search
          </button>
        </form>

        {/* Quick Action Navigation Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
          <Link
            to="/"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-2.5 bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 text-xs font-bold rounded-xl transition-colors"
          >
            <Home className="w-3.5 h-3.5" />
            <span>Return Home</span>
          </Link>

          <Link
            to="/explore"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-2.5 bg-teal-800 hover:bg-teal-900 text-white text-xs font-bold rounded-xl transition-colors shadow-xs"
          >
            <Compass className="w-3.5 h-3.5 text-emerald-300" />
            <span>Explore All Schemes</span>
          </Link>

          <Link
            to="/survey"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-2.5 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-slate-950 font-black text-xs rounded-xl transition-all shadow-xs"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Check Eligibility</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>
    </div>
  );
};

export default NotFoundPage;
