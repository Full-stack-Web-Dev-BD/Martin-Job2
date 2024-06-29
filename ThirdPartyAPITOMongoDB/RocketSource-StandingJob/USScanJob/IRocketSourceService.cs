namespace RocketSource
{
    public interface IRocketSourceService
    {
        void ProcessScans();
        void GetScanResult(int scanId);
    }
}